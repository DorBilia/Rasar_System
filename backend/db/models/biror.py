"""Biror (clarification/disciplinary) models and lookup tables."""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base

__all__ = ["Biror", "BirorResult", "BirorType"]


class BirorType(Base):
    __tablename__ = "biror_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    biror_type_description: Mapped[str] = mapped_column(String(255), nullable=False)

    birors: Mapped[List["Biror"]] = relationship(back_populates="biror_type_ref")

    def __repr__(self) -> str:
        return f"BirorType(id={self.id!r})"


class BirorResult(Base):
    __tablename__ = "biror_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    biror_result_description: Mapped[str] = mapped_column(String(255), nullable=False)

    birors: Mapped[List["Biror"]] = relationship(back_populates="biror_result_ref")

    def __repr__(self) -> str:
        return f"BirorResult(id={self.id!r})"


class Biror(Base):
    __tablename__ = "birors"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)

    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.id", ondelete="RESTRICT"), nullable=False
    )
    biror_type: Mapped[int] = mapped_column(
        ForeignKey("biror_types.id", ondelete="RESTRICT"), nullable=False
    )
    biror_date: Mapped[date] = mapped_column(Date, nullable=False)
    biror_description: Mapped[str] = mapped_column(Text)
    comments: Mapped[Optional[str]] = mapped_column(Text)
    biror_result: Mapped[int] = mapped_column(
        ForeignKey("biror_results.id", ondelete="RESTRICT")
    )

    soldier: Mapped["Soldier"] = relationship(back_populates="birors")
    biror_type_ref: Mapped["BirorType"] = relationship(back_populates="birors")
    biror_result_ref: Mapped["BirorResult"] = relationship(back_populates="birors")

    def __repr__(self) -> str:
        return f"Biror(id={self.id!r})"
