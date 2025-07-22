"""
Database package initializer.

Exposes:
    - Base       : Declarative base class for ORM models.
    - get_db     : FastAPI dependency that yields an AsyncSession.
    - engine     : Shared SQLAlchemy AsyncEngine instance.
"""
from .base import Base                     # noqa: F401
from .session import engine, get_db        # noqa: F401
