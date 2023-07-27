from abc import ABC, abstractmethod

from app.core.zara.models import Product, ProductColor, ProductSize
from app.db import AsyncSession
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


class ProductPGRepo(ProductRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__()
        self.db_session = db_session

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
        await self.batch_save_sizes(list(sizes_map.values()))
        await self.batch_save_colors(list(colors_map.values()))
        await self.batch_save_products(list(products_map.values()))
        await self.batch_create_product_color(list(products_map.values()))
        await self.batch_create_product_color_images(list(products_map.values()))
        await self.batch_create_product_color_sizes(list(products_map.values()))
        await self.db_session.commit()

    async def batch_save_sizes(self, sizes: list[ProductSize]):
        data = [{'id': s.id, 'name': s.name} for s in sizes]
        query = (
            insert(sizes_table)
            .values(data)
            .on_conflict_do_nothing(index_elements=["id"])
        )
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def batch_save_colors(self, colors: list[ProductColor]):
        data = [{'id': c.id, 'name': c.name, 'hex_code': c.hexCode} for c in colors]
        query = (
            insert(colors_table)
            .values(data)
            .on_conflict_do_nothing(index_elements=["id"])
        )
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def batch_save_products(self, products: list[Product]):
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

    async def batch_create_product_color(self, products: list[Product]) -> None:
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

    async def batch_create_product_color_images(self, products: list[Product]) -> None:
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

    async def batch_create_product_color_sizes(self, products: list[Product]) -> None:
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
