import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.config import PG_DATABASE_URL, MSSQL_DATABASE_URL
from api_erp.utils.models import Base
from core.logger import logging_config

logger = logging.getLogger(__name__)
logging_config(level=logging.INFO)

pg_engine = create_async_engine(PG_DATABASE_URL, echo=True)
pg_async_session_maker = async_sessionmaker(pg_engine, class_=AsyncSession, expire_on_commit=False)

mssql_engine = create_async_engine(MSSQL_DATABASE_URL, echo=True)
mssql_async_session_maker = async_sessionmaker(mssql_engine, class_=AsyncSession, expire_on_commit=False)


async def get_pg_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with pg_async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_mssql_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with mssql_async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_pg_db():
    async with pg_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


