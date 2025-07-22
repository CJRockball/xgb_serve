"""
Async SQLAlchemy session management.

Provides:
    • `engine`             – shared AsyncEngine with sensible pool settings.
    • `AsyncSessionLocal`  – sessionmaker factory.
    • `get_db()`           – FastAPI dependency that yields an AsyncSession.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# --------------------------------------------------------------------------- #
# Engine                                                                      #
# --------------------------------------------------------------------------- #
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
    pool_timeout=30,
    echo=False,              # change to True for verbose SQL logging
    future=True,
)

# --------------------------------------------------------------------------- #
# Session factory                                                             #
# --------------------------------------------------------------------------- #
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# --------------------------------------------------------------------------- #
# FastAPI dependency                                                          #
# --------------------------------------------------------------------------- #
@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields an AsyncSession and guarantees proper close/rollback.

    Usage:
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            # SQLAlchemy automatically rolls back any uncommitted transaction
            await session.close()
