from __future__ import annotations

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base

__all__ = ["Branch", "Section", "Unit"]

from db.models import Soldier


class Unit(Base):
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    soldiers: Mapped[List["Soldier"]] = relationship(back_populates="unit_ref")

    def __repr__(self) -> str:
        return f"Unit(id={self.id!r})"


class Branch(Base):
    __tablename__ = "branches"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    soldiers: Mapped[List["Soldier"]] = relationship(back_populates="branch_ref")

    def __repr__(self) -> str:
        return f"Branch(id={self.id!r})"


class Section(Base):
    __tablename__ = "sections"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    soldiers: Mapped[List["Soldier"]] = relationship(back_populates="sections_ref")

    def __repr__(self) -> str:
        return f"Section(id={self.id!r})"
