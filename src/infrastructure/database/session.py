import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import Union

db = sa.create_engine(settings.database.url, echo=True)
Session = sessionmaker(bind=db)
Base = declarative_base()

# Add async setup
async_engine = create_async_engine(settings.database.async_url, echo=True)
AsyncSession = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


def get_session_factory(use_async: bool = settings.database.is_async) -> Union[sessionmaker, async_sessionmaker]:
    """Return either AsyncSession or Session based on use_async flag"""
    return AsyncSession if use_async else Session