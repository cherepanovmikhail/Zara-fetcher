from app.core.zara.client import Countries, ZaraClient
from app.storage.db import create_engine, dispose_engine, get_session_maker
from app.storage.db.repositories import ProductPGRepo


async def fetch_data() -> None:
    db_engine = await create_engine()
    db_session = await get_session_maker(db_engine)
    async with db_session() as session:
        client = ZaraClient(country=Countries.thailand)
        products = client.get_products()
        repo = ProductPGRepo(db_session=session)
        await repo.batch_save(products)

    await dispose_engine(db_engine)
