"""Biror (clarification/disciplinary) models and lookup tables."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from core.enums import BirorResultEnum, BirorTypeEnum

__all__ = ["Biror", "BirorResult", "BirorType"]

if TYPE_CHECKING:
    from db.models.Soldier import Soldier


class BirorType(Base):
    __tablename__ = "biror_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    biror_type_description: Mapped[BirorTypeEnum] = mapped_column(
        SAEnum(BirorTypeEnum, native_enum=False),
        nullable=False,
    )

    birors: Mapped[List["Biror"]] = relationship(back_populates="biror_type_ref")

    def __repr__(self) -> str:
        return f"BirorType(id={self.id!r})"


class BirorResult(Base):
    __tablename__ = "biror_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    biror_result_description: Mapped[BirorResultEnum] = mapped_column(
        SAEnum(BirorResultEnum, native_enum=False), nullable=False
    )

    birors: Mapped[List["Biror"]] = relationship(back_populates="biror_result_ref")

    def __repr__(self) -> str:
        return f"BirorResult(id={self.id!r})"


class Biror(Base):
    __tablename__ = "birors"

    id: Mapped[int] = mapped_column(primary_key=True)

    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.soldier_id", ondelete="RESTRICT"), nullable=False
    )
    biror_type: Mapped[int] = mapped_column(
        ForeignKey("biror_types.biror_type_id", ondelete="RESTRICT"), nullable=False
    )
    biror_date: Mapped[date] = mapped_column(Date, nullable=False)
    biror_description: Mapped[str] = mapped_column(Text, nullable=False)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    biror_result: Mapped[int] = mapped_column(
        ForeignKey("biror_results.biror_result_id", ondelete="RESTRICT"), nullable=False
    )

    soldier: Mapped["Soldier"] = relationship(back_populates="birors")
    biror_type_ref: Mapped["BirorType"] = relationship(back_populates="birors")
    biror_result_ref: Mapped["BirorResult"] = relationship(back_populates="birors")

    def __repr__(self) -> str:
        return f"Biror(biror_id={self.biror_id!r})"
