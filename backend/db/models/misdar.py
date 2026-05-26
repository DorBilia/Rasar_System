"""Misdar (roll call) definitions and attendance scanning records."""

from __future__ import annotations

from datetime import date, time
from typing import List

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String, Time, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from core.enums import MisdarNameEnum, DayOfWeek

__all__ = ["MisdarAttendance", "MisdarType", "MisdarTypeDays"]


class MisdarType(Base):
    __tablename__ = "misdar_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    misdar_name: Mapped[MisdarNameEnum] = mapped_column(
        SAEnum(MisdarNameEnum, native_enum=False), nullable=False
    )
    misdar_time: Mapped[time] = mapped_column(Time, nullable=False)
    misdar_length: Mapped[float] = mapped_column(Float)

    misdars: Mapped[List["MisdarAttendance"]] = relationship(back_populates="misdar_type_ref")
    misdar_mappings: Mapped[List["IndicationTypeMisdarType"]] = relationship(
        "IndicationTypeMisdarType", back_populates="misdar_type"
    )
    misdar_days: Mapped[List["MisdarTypeDays"]] = relationship(
        back_populates="misdar_type_ref", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"MisdarType(id={self.id!r})"


class MisdarTypeDays(Base):
    __tablename__ = "misdar_type_days"
    misdar_type: Mapped[int] = mapped_column(ForeignKey("misdar_types.id"), primary_key=True)
    misdar_day: Mapped[DayOfWeek] = mapped_column(
        SAEnum(DayOfWeek, native_enum=False), primary_key=True
    )

    misdar_type_ref: Mapped["MisdarType"] = relationship(back_populates="misdar_days")

    def __repr__(self) -> str:
        return f"MisdarTypeDays(misdar_type={self.misdar_type!r}, misdar_day={self.misdar_day!r})"


class MisdarAttendance(Base):
    __tablename__ = "misdar_attendance"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.id", ondelete="RESTRICT"), nullable=False
    )
    misdar_type: Mapped[int] = mapped_column(
        ForeignKey("misdar_types.id", ondelete="RESTRICT"), nullable=False
    )
    misdar_date: Mapped[date] = mapped_column(Date, nullable=False)
    scan_time: Mapped[time] = mapped_column(Time, nullable=False)

    scan_note: Mapped[str] = mapped_column(String(255), nullable=False)
    # A log about the can status - succesful/conflict with indication

    soldier: Mapped["Soldier"] = relationship(back_populates="misdar_attendance_records")
    misdar_type_ref: Mapped["MisdarType"] = relationship(back_populates="misdars")

    def __repr__(self) -> str:
        return f"Misdar(misdar_date={self.misdar_date!r},misdar_type={self.misdar_type!r})"
