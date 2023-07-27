from pydantic import BaseModel, Field, conint


ProductId = conint(gt=0)
CategoryId = conint(gt=0)
ColorId = conint(gt=0)
StylingId = conint(ge=0)
SizeId = conint(gt=0)
Price = conint(gt=0)
SKU = conint(gt=0)


class Image(BaseModel):
    datatype: str
    set: int
    type: str
    kind: str
    path: str
    name: str
    width: int
    height: int
    timestamp: str
    order: int = Field(default=1)

    @property
    def url(self) -> str:
        base = "https://static.zara.net/photos"
        return f"{base}{self.path}/w/{self.width}/{self.name}.jpg?ts={self.timestamp}"


class ProductSeo(BaseModel):
    keyword: str
    description: str
    seoProductId: str
    discernProductId: int


class Brand(BaseModel):
    brandId: int
    brandGroupId: int
    brandGroupCode: str


class ProductSize(BaseModel):
    availability: str
    equivalentSizeId: int
    id: SizeId
    name: str
    price: Price
    reference: str
    sku: SKU
    demand: str


class ProductColor(BaseModel):
    id: ColorId
    hexCode: str
    productId: ProductId
    name: str
    reference: str
    stylingId: StylingId
    xmedia: list[Image]
    sizes: list[ProductSize]
    price: Price
    description: str
    rawDescription: str


class ProductDetails(BaseModel):
    reference: str
    displayReference: str
    colors: list[ProductColor]


class Product(BaseModel):
    id: ProductId
    category_id: CategoryId
    currency: str
    type: str
    kind: str
    state: str
    brand: Brand
    name: str
    detail: ProductDetails
    seo: ProductSeo


class CommercialComponent(BaseModel):
    id: ProductId
    type: str


class ProductGroupElement(BaseModel):
    id: str
    type: str | None = Field(default=None)
    layout: str | None = Field(default=None)
    commercial_components: list[CommercialComponent] = Field(
        alias='commercialComponents', default=[]
    )


class ProductGroup(BaseModel):
    id: str
    type: str
    elements: list[ProductGroupElement]


class CategoryResponse(BaseModel):
    product_groups: list[ProductGroup] = Field(alias='productGroups')
