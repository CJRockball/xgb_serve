"""
Declarative base class definition.

• All ORM model classes must inherit from Base.
• A lightweight `to_dict` helper is provided for easy JSON serialisation.
"""
from typing import Any, Dict
from sqlalchemy.orm import DeclarativeMeta, declarative_base


class _CustomBase:
    """Mixin that injects common helpers into every model."""

    def to_dict(self) -> Dict[str, Any]:
        """Return a plain-Python dict of column names → values."""
        return {
            column.key: getattr(self, column.key)
            for column in self.__table__.columns            # type: ignore[attr-defined]
        }

    def __repr__(self) -> str:                              # noqa: D401
        """Human-readable representation."""
        pk = getattr(self, "id", None)
        return f"<{self.__class__.__name__} id={pk!s}>"


# Declarative base used across the project
Base: DeclarativeMeta = declarative_base(cls=_CustomBase)   # type: ignore[valid-type]
