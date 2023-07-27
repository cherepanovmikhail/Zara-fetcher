from abc import ABC, abstractmethod

from app.core.schemas import Limit, Page, ProductDetailed, ProductListItem, ProductsList
from app.core.zara.models import Product, ProductColor, ProductId, ProductSize
from app.db import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from .tables import (
    colors_table,
    product_colors_images_table,
    product_colors_sizes_table,
    product_colors_table,
    products_table,
    sizes_table,
)


class ProductRepo(ABC):
    @abstractmethod
    async def batch_save(self, products: list[Product]):
        ...

    @abstractmethod
    async def get_by_id(self, product_id: ProductId) -> ProductDetailed | None:
        ...

    @abstractmethod
    async def get_all(self, page: Page, limit: Limit) -> ProductsList:
        ...


class ProductPGRepo(ProductRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__()
        self.db_session = db_session

    async def get_by_id(self, product_id: ProductId) -> ProductDetailed | None:
        query = (
            select(
                product_colors_table.c.id,
                products_table.c.name,
                product_colors_table.c.price,
                colors_table.c.name.label('color'),
                product_colors_table.c.description,
            )
            .select_from(product_colors_table.join(products_table).join(colors_table))
            .where(product_colors_table.c.id == product_id)
        )

        data = (await self.db_session.execute(query)).mappings().fetchone()
        data = {**data, 'price': data['price'] / 100}
        if data:
            data = ProductDetailed.model_validate(data)
        return data

    async def get_all(self, page: Page, limit: Limit) -> ProductsList:
        offset = (page - 1) * limit
        query = (
            select(
                product_colors_table.c.id,
                products_table.c.name,
                product_colors_table.c.price,
                colors_table.c.name.label('color'),
            )
            .select_from(product_colors_table.join(products_table).join(colors_table))
            .order_by(products_table.c.name.asc(), product_colors_table.c.price.asc())
            .offset(offset=offset)
            .limit(limit=limit)
        )
        data = (await self.db_session.execute(query)).mappings().fetchall()

        data = ({**d, 'price': d['price'] / 100} for d in data)

        return ProductsList(
            page=page,
            limit=limit,
            products=[ProductListItem.model_validate(d) for d in data],
        )

    async def batch_save(self, products: list[Product]):
        sizes_map = {}
        colors_map = {}
        products_map = {}
        images_map = {}
        for product in products:
            products_map[product.id] = product
            for color in product.detail.colors:
                for image in color.xmedia:
                    images_map[image.path + image.name] = image
                colors_map[color.id] = color
                for size in color.sizes:
                    sizes_map[size.id] = size
        await self.__batch_save_sizes(list(sizes_map.values()))
        await self.__batch_save_colors(list(colors_map.values()))
        await self.__batch_save_products(list(products_map.values()))
        await self.__batch_create_product_color(list(products_map.values()))
        await self.__batch_create_product_color_images(list(products_map.values()))
        await self.__batch_create_product_color_sizes(list(products_map.values()))
        await self.db_session.commit()

    async def __batch_save_sizes(self, sizes: list[ProductSize]):
        data = [{'id': s.id, 'name': s.name} for s in sizes]
        query = (
            insert(sizes_table)
            .values(data)
            .on_conflict_do_nothing(index_elements=["id"])
        )
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def __batch_save_colors(self, colors: list[ProductColor]):
        data = [{'id': c.id, 'name': c.name, 'hex_code': c.hexCode} for c in colors]
        query = (
            insert(colors_table)
            .values(data)
            .on_conflict_do_nothing(index_elements=["id"])
        )
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def __batch_save_products(self, products: list[Product]):
        data = [
            {
                'id': p.id,
                'name': p.name,
                'seo_keyword': p.seo.keyword,
                'seo_product_id': p.seo.seoProductId,
                'discern_product_id': p.seo.discernProductId,
            }
            for p in products
        ]
        query = (
            insert(products_table)
            .values(data)
            .on_conflict_do_nothing(index_elements=["id"])
        )
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def __batch_create_product_color(self, products: list[Product]) -> None:
        data = []
        for product in products:
            for color in product.detail.colors:
                data.append(
                    {
                        "id": color.productId,
                        "product_id": product.id,
                        "color_id": color.id,
                        "price": color.price,
                        "description": color.description,
                        "rawDescription": color.rawDescription,
                    }
                )
        query = (
            insert(product_colors_table)
            .values(data)
            .on_conflict_do_update(index_elements=["id"], set_=product_colors_table.c)
        )
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def __batch_create_product_color_images(
        self, products: list[Product]
    ) -> None:
        data = []
        # TODO maybe need to add remove previous relations
        for product in products:
            for color in product.detail.colors:
                for image in color.xmedia:
                    data.append(
                        {
                            "product_color_id": color.productId,
                            "path": image.path,
                            "name": image.name,
                            "width": image.width,
                            "height": image.height,
                            "timestamp": image.timestamp,
                        }
                    )
        query = (
            insert(product_colors_images_table)
            .values(data)
            .on_conflict_do_update(
                index_elements=["product_color_id", "path", "name"],
                set_=product_colors_images_table.c,
            )
        )
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def __batch_create_product_color_sizes(self, products: list[Product]) -> None:
        data = []
        # TODO maybe need to add remove previous relations
        for product in products:
            for color in product.detail.colors:
                for size in color.sizes:
                    data.append(
                        {
                            "sku": size.sku,
                            "product_color_id": color.productId,
                            "size_id": size.id,
                            "availability": size.availability,
                            "price": size.price,
                            "demand": size.demand,
                        }
                    )
        query = (
            insert(product_colors_sizes_table)
            .values(data)
            .on_conflict_do_update(
                index_elements=["sku"], set_=product_colors_sizes_table.c
            )
        )
        await self.db_session.execute(query)
        await self.db_session.commit()
