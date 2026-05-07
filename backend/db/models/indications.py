"""Indications attached to soldiers (exemptions, punishment, late arrival, etc.)."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, List

from sqlalchemy import Date, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from core.enums import IndicationDescriptionEnum

if TYPE_CHECKING:
    from db.models.soldier import Soldier

__all__ = ["Indication", "IndicationType"]


class IndicationType(Base):
    __tablename__ = "indication_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    indication_description: Mapped[IndicationDescriptionEnum] = mapped_column(
        SAEnum(IndicationDescriptionEnum, native_enum=False), nullable=False
    )
    weekly_arrivals: Mapped[int] = mapped_column(nullable=False)

    indications: Mapped[List["Indication"]] = relationship(back_populates="indication_type_ref")

    def __repr__(self) -> str:
        return f"IndicationType(id={self.id!r})"


class Indication(Base):
    __tablename__ = "indications"

    id: Mapped[int] = mapped_column(primary_key=True)

    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.soldier_id", ondelete="RESTRICT"), nullable=False
    )
    indication_type: Mapped[int] = mapped_column(
        ForeignKey("indication_types.indication_type_id", ondelete="RESTRICT"),
        nullable=False,
    )
    indication_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    indication_end_date: Mapped[date] = mapped_column(Date, nullable=False)

    soldier: Mapped["Soldier"] = relationship(back_populates="indications")
    indication_type_ref: Mapped["IndicationType"] = relationship(back_populates="indications")

    def __repr__(self) -> str:
        return f"Indication(indication_id={self.indication_id!r})"