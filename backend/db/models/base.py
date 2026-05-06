"""SQLAlchemy base definitions for the Rasar domain models.

This module defines the SQLAlchemy 2.0 Declarative Base used by all models in
`backend.db.models`. It intentionally contains no business logic.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""

