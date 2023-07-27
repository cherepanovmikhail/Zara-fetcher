from app.core.zara.models import ProductId
from pydantic import BaseModel, conint


Page = conint(gt=0)
Limit = conint(gt=0, lt=30)


class Paginated(BaseModel):
    page: Page
    limit: Limit


class ProductListItem(BaseModel):
    id: ProductId
    name: str
    price: float
    color: str


class ProductsList(Paginated):
    products: list[ProductListItem]


class ProductDetailed(BaseModel):
    id: ProductId
    name: str
    price: float
    color: str
    description: str
