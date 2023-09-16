from typing import Generator

from config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)
sync_engine = create_engine(settings.DATABASE_URL_ALEMBIC, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    except:
        await session.close()
