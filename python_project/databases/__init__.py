from asyncio import current_task

from settings import postgres_settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    postgres_settings.URI,
    pool_size=postgres_settings.POOL_SIZE,
    max_overflow=postgres_settings.MAX_OVERFLOW,
)

async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Session = async_scoped_session(async_session_factory, scopefunc=current_task)
Base = declarative_base()

from .models import *
