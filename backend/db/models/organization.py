"""Organization hierarchy models (units, branches, departments).

Defines the organizational structure used by the Rasar system.
"""

from __future__ import annotations

from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True)
    unit_name: Mapped[str] = mapped_column(String(255), nullable=False)

    branches: Mapped[List["Branch"]] = relationship(back_populates="unit")

    def __repr__(self) -> str:
        return f"Unit(id={self.id!r})"


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)
    unit_id: Mapped[int] = mapped_column(
        ForeignKey("units.id", ondelete="RESTRICT"), nullable=False
    )
    branch_name: Mapped[str] = mapped_column(String(255), nullable=False)

    unit: Mapped["Unit"] = relationship(back_populates="branches")
    departments: Mapped[List["Department"]] = relationship(back_populates="branch")

    def __repr__(self) -> str:
        return f"Branch(id={self.id!r})"


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id", ondelete="RESTRICT"), nullable=False
    )
    department_name: Mapped[str] = mapped_column(String(255), nullable=False)

    branch: Mapped["Branch"] = relationship(back_populates="departments")

    def __repr__(self) -> str:
        return f"Department(id={self.id!r})"

