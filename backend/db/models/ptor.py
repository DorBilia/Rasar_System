
from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from core.enums import BeardStatementTypeEnum

__all__ = ["BeardStatement", "BeardStatementType", "MedicalPtor", "MedicalPtorType"]

from db.models.soldier import Soldier


class MedicalPtorType(Base):
    __tablename__ = "medical_ptor_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    med_ptor_description: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"MedicalPtorType(id={self.id!r})"


class MedicalPtor(Base):
    __tablename__ = "medical_ptors"

    id: Mapped[int] = mapped_column(primary_key=True)

    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.id", ondelete="RESTRICT"), nullable=False
    )
    med_ptor_type: Mapped[int] = mapped_column(
        ForeignKey("medical_ptor_types.id", ondelete="RESTRICT"),
        nullable=False,
    )
    given_by: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    soldier: Mapped["Soldier"] = relationship(back_populates="medical_ptors")
    medical_ptor_type: Mapped["MedicalPtorType"] = relationship()

    def __repr__(self) -> str:
        return f"MedicalPtor(id={self.id!r})"


class BeardStatementType(Base):
    __tablename__ = "beard_statement_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[BeardStatementTypeEnum] = mapped_column(
        SAEnum(BeardStatementTypeEnum, native_enum=False), nullable=False
    )

    def __repr__(self) -> str:
        return (
            "BeardStatementType("
            f"id={self.id!r}"
            ")"
        )


class BeardStatement(Base):
    __tablename__ = "beard_statements"

    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.id", ondelete="RESTRICT"), primary_key=True
    )
    beard_statement_type: Mapped[int] = mapped_column(
        ForeignKey("beard_statement_types.id", ondelete="RESTRICT"),
        nullable=False,
    )
    is_canceled: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    cancelation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    statements_start_date: Mapped[date] = mapped_column(Date, nullable=False)

    soldier: Mapped["Soldier"] = relationship(back_populates="beard_statements")
    beard_statement_type_ref: Mapped["BeardStatementType"] = relationship()

    def __repr__(self) -> str:
        return f"BeardStatement(soldier_id={self.soldier_id!r})"