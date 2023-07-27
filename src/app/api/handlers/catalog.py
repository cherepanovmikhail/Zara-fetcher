from fastapi import APIRouter


router = APIRouter(tags=["catalog"], prefix='/catalog')


@router.get("/")
def get_all_goods():
    return {}
