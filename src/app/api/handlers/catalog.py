from app.core.schemas import Limit, Page, ProductDetailed, ProductsList
from app.core.zara.models import ProductId
from dependencies import ProductRepo, products_repo
from fastapi import APIRouter, Depends, HTTPException, Query, status


router = APIRouter(tags=["catalog"], prefix='/catalog')


@router.get(
    "/products",
    response_model=ProductsList,
    summary="Получить список доступных товаров",
)
async def get_all_products(
    page: Page = Query(Page(1), gt=0),
    limit: Limit = Query(Limit(10), gt=0, lt=30),
    repo: ProductRepo = Depends(products_repo),
):
    return await repo.get_all(page=page, limit=limit)


@router.get(
    "/products/{product_id}",
    response_model=ProductDetailed,
    summary="Получить детальную информацию о товаре",
)
async def get_product_by_id(
    product_id: ProductId,
    repo: ProductRepo = Depends(products_repo),
):
    product = await repo.get_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'product with id {product_id} not found',
        )
    return product
