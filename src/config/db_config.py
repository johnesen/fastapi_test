from typing import Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings
from databases import Database

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

database = Database(settings.DATABASE_URL)
Base = declarative_base()


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    except:
        await session.close()

