from app.settings import DBSettings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


db_settings = DBSettings()


async def create_engine():
    engine = create_async_engine(
        db_settings.async_dsn,
        echo=True,
    )

    print(f'engine {id(engine)} created')
    return engine


async def dispose_engine(engine):
    print(f'engine {id(engine)} disposed')
    await engine.dispose()


async def get_session_maker(engine) -> AsyncSession:
    return async_sessionmaker(engine, expire_on_commit=False)
