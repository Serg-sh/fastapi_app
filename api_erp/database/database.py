from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker

from api_erp.config import MSSQL_DB_SERVER, MSSQL_DB_NAME, MSSQL_DB_USER, MSSQL_DB_PASS
from api_erp.config import PG_DB_SERVER, PG_DB_NAME, PG_DB_USER, PG_DB_PASS

MSSQL_DATABASE_URL = (
    f'mssql+aioodbc://{MSSQL_DB_USER}:{MSSQL_DB_PASS}@{MSSQL_DB_SERVER}/{MSSQL_DB_NAME}?driver=ODBC Driver 17 for SQL '
    f'Server&MARS_Connection=Yes')

PG_DATABASE_URL = f"postgresql+asyncpg://{PG_DB_USER}:{PG_DB_PASS}@{PG_DB_SERVER}/{PG_DB_NAME}"

Base = declarative_base()

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
