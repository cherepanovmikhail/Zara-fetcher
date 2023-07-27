from dependencies import AsyncSession, db_session
from fastapi import APIRouter, Depends
from sqlalchemy import text


router = APIRouter(tags=["healthcheck"], prefix='/health')


@router.get("/alive")
async def get_service_alive():
    return {}


@router.get("/ready")
async def get_service_ready(session: AsyncSession = Depends(db_session)):
    res = await session.execute(text('select 1'))
    return {'db': await res.fetchone()}
