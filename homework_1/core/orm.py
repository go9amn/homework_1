from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.settings.settings import settings


async_engine = create_async_engine(
    settings.db.url,
    echo=True,
    connect_args=dict(prepared_statement_cache_size=0),
)
async_db_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base = declarative_base()


async def create_db_session() -> AsyncSession:
    '''Генератор для создания объекта асинхронной сессии'''
    async with async_db_session() as db_session:
        yield db_session
