from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import settings

engine = create_async_engine(settings.DATABASE_URL)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


@asynccontextmanager
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
