import random
from enum import Enum, StrEnum

import httpx
from pydantic import BaseModel

from .models import CategoryResponse, Product, ProductId


class Currencies(Enum):
    thb = 'THB'
    gbp = 'GBP'


class Languages(StrEnum):
    en = 'en'


class Config(BaseModel):
    code: str
    currency: Currencies
    lang: Languages


class Countries(Enum):
    thailand = Config(code='th', currency=Currencies.thb, lang=Languages.en)
    uk = Config(code='uk', currency=Currencies.gbp, lang=Languages.en)


class ZaraClient:
    def __init__(self, country: Countries) -> None:
        self._config = country.value

    @property
    def headers(self) -> dict:
        return {
            "Host": "www.zara.com",
            "Referer": "https://www.zara.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) Version/16.5.2 Safari/605.1.15",
        }

    def __get_products_ids(self, category_id: int) -> list[ProductId]:
        url = f"https://www.zara.com/{self._config.code}/{self._config.lang}/category/{category_id}/products"
        response = httpx.get(url, params={'ajax': 'true'}, headers=self.headers)
        response.raise_for_status()
        response_data = CategoryResponse.model_validate(response.json())
        result = set()
        for group in response_data.product_groups:
            for element in group.elements:
                for component in element.commercial_components:
                    if component.type == 'Product':
                        result.add(ProductId(component.id))
        return sorted(result)

    def __get_products_details(
        self, product_ids: list[ProductId], category_id: int, batch_size=10
    ) -> list[Product]:
        url = f"https://www.zara.com/{self._config.code}/{self._config.lang}/products-details"
        result = {}
        processed_ids_set = set()

        while len(product_ids):
            print(len(product_ids))
            random.shuffle(product_ids)
            params = {'productIds': product_ids[:batch_size], 'ajax': 'true'}
            response = httpx.get(url, params=params, headers=self.headers)
            response.raise_for_status()

            for product_data in response.json():
                product_data['category_id'] = category_id
                product_data['currency'] = self._config.currency.value
                product = Product.model_validate(product_data)
                print(product.id, sum([1 for color in product.detail.colors]))
                if product.id not in result:
                    result[product.id] = product

                    for color in product.detail.colors:
                        processed_ids_set.add(color.productId)

            product_ids = [i for i in product_ids if i not in processed_ids_set]
            print(sum([len(p.detail.colors) for p in result.values()]))
        return list(result.values())

    def get_products(self, category_id: int = 2297840) -> list[Product]:
        product_ids = self.__get_products_ids(category_id=category_id)
        return self.__get_products_details(product_ids, category_id)
