import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine
from db_queries.dg_data import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True
    #pool_size=5,
    #max_overflow=10
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
    #pool_size=5,
    #max_overflow=10
)

session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)

def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close

class Base(DeclarativeBase):
    pass