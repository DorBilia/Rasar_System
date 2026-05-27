"""Indications attached to soldiers (exemptions, punishment, late arrival, etc.)."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, List

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from core.enums import IndicationDescriptionEnum

if TYPE_CHECKING:
    from db.models.soldier import Soldier

__all__ = ["Indication", "IndicationType", "IndicationTypeMisdarType", "OrganizationIndication"]


class IndicationType(Base):
    __tablename__ = "indication_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    indication_description: Mapped[IndicationDescriptionEnum] = mapped_column(
        SAEnum(IndicationDescriptionEnum, native_enum=False), nullable=False
    )
    weekly_arrivals: Mapped[int] = mapped_column(nullable=False)

    indications: Mapped[List["Indication"]] = relationship(back_populates="indication_type_ref")
    indication_mappings: Mapped[List["IndicationTypeMisdarType"]] = relationship(
        "IndicationTypeMisdarType", back_populates="indication_type"
    )

    def __repr__(self) -> str:
        return f"IndicationTypeSchema(id={self.id!r})"


class IndicationTypeMisdarType(Base):
    __tablename__ = "indication_types_misdar_types"
    indication_type_id: Mapped[int] = mapped_column(ForeignKey("indication_types.id"), primary_key=True)
    misdar_type_id: Mapped[int] = mapped_column(ForeignKey("misdar_types.id"), primary_key=True)

    misdar_type: Mapped["MisdarType"] = relationship(back_populates="misdar_mappings")
    indication_type: Mapped["IndicationType"] = relationship(back_populates="indication_mappings")

    def __repr__(self) -> str:
        return f"IndicationTypeMisdarType(indication_type_id={self.indication_type!r},misdar_type_id={self.misdar_type_id!r})"


class Indication(Base):
    __tablename__ = "indications"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)

    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.id", ondelete="RESTRICT"), nullable=False
    )
    indication_type: Mapped[int] = mapped_column(ForeignKey("indication_types.id", ondelete="RESTRICT"),
                                                 nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization_indications.id", ondelete="RESTRICT"),
                                                 nullable=True)
    # uuid to distinguish organized indications from specific indications

    soldier: Mapped["Soldier"] = relationship(back_populates="indications")
    indication_type_ref: Mapped["IndicationType"] = relationship(back_populates="indications")
    organization: Mapped["OrganizationIndication"] = relationship(back_populates="indications")

    def __repr__(self) -> str:
        return f"Indication(id={self.id!r})"


class OrganizationIndication(Base):
    __tablename__ = "organization_indications"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id", ondelete="RESTRICT"), nullable=True)
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id", ondelete="RESTRICT"), nullable=True)
    indication_type: Mapped[int] = mapped_column(ForeignKey("indication_types.id", ondelete="RESTRICT"),
                                                 nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    indications: Mapped[List["Indication"]] = relationship(back_populates="organization", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"OrganizationIndication (id={self.id!r})"
