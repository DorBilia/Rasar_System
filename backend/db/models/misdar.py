"""Misdar (roll call) definitions and attendance scanning records."""

from __future__ import annotations

from datetime import date, time
from typing import List

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String, Time, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.soldier import Soldier

from db.db import Base
from core.enums import MisdarNameEnum

__all__ = ["MisdarAttendance", "MisdarType"]


class MisdarType(Base):
    __tablename__ = "misdar_types"

    misdar_type_id: Mapped[int] = mapped_column(primary_key=True)
    misdar_name: Mapped[MisdarNameEnum] = mapped_column(
        SAEnum(MisdarNameEnum, native_enum=False), nullable=False
    )
    weekly_arrivals: Mapped[int] = mapped_column(nullable=False)
    misdar_time: Mapped[time] = mapped_column(Time, nullable=False)
    misdar_length: Mapped[float] = mapped_column(Float)

    misdars: Mapped[List["MisdarAttendance"]] = relationship(back_populates="misdar_type_ref")

    def __repr__(self) -> str:
        return f"MisdarType(misdar_type_id={self.misdar_type_id!r})"


class MisdarAttendance(Base):
    __tablename__ = "misdar_attendance"

    misdar_id: Mapped[int] = mapped_column(primary_key=True)
    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.soldier_id", ondelete="RESTRICT"), nullable=False
    )
    misdar_type: Mapped[int] = mapped_column(
        ForeignKey("misdar_types.misdar_type_id", ondelete="RESTRICT"), nullable=False
    )
    misdar_date: Mapped[date] = mapped_column(Date, nullable=False)
    scan_time: Mapped[time] = mapped_column(Time, nullable=False)

    scan_note: Mapped[str] = mapped_column(String(255), nullable=False)
    # A log about the can status - succesful/conflict with indication

    soldier: Mapped["Soldier"] = relationship(back_populates="misdars")
    misdar_type_ref: Mapped["MisdarType"] = relationship(back_populates="misdars")

    def __repr__(self) -> str:
        return f"Misdar(misdar_id={self.misdar_id!r})"
