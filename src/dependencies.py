from contextlib import asynccontextmanager
from typing import Generator

from app.storage.db import (
    AsyncSession,
    create_engine,
    dispose_engine,
    get_session_maker,
)
from fastapi import FastAPI, Request


async def db_session(request: Request) -> Generator[AsyncSession, None, None]:
    async with request.app.state.db_session() as session:
        print(f'created new session {id(session)}')
        yield session
        print(f'purged session {id(session)}')


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_engine = await create_engine()
    # run_sql_migrations()
    app.state.db_session = await get_session_maker(app.state.db_engine)
    yield
    await dispose_engine(app.state.db_engine)
