"""Misdar (roll call) definitions and attendance scanning records."""

from __future__ import annotations

from datetime import date, time
from typing import List

from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, String, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from db.models.enums import MisdarNameEnum


class MisdarType(Base):
    __tablename__ = "misdar_types"

    misdar_type_id: Mapped[int] = mapped_column(primary_key=True)
    misdar_name: Mapped[MisdarNameEnum] = mapped_column(
        SAEnum(MisdarNameEnum, native_enum=False), nullable=False
    )
    weekly_arrivals: Mapped[int] = mapped_column(nullable=False)
    misdar_time: Mapped[time] = mapped_column(Time, nullable=False)

    misdars: Mapped[List["Misdar"]] = relationship(back_populates="misdar_type_ref")

    def __repr__(self) -> str:
        return f"MisdarType(misdar_type_id={self.misdar_type_id!r})"


class Misdar(Base):
    __tablename__ = "misdars"

    misdar_id: Mapped[int] = mapped_column(primary_key=True)
    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.soldier_id", ondelete="RESTRICT"), nullable=False
    )
    misdar_type: Mapped[int] = mapped_column(
        ForeignKey("misdar_types.misdar_type_id", ondelete="RESTRICT"), nullable=False
    )
    misdar_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_open: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    scan_note: Mapped[str] = mapped_column(String(255), nullable=False)

    soldier: Mapped["Soldier"] = relationship(back_populates="misdars")
    misdar_type_ref: Mapped["MisdarType"] = relationship(back_populates="misdars")
    attendance_records: Mapped[List["MisdarAttendanceRecord"]] = relationship(
        back_populates="misdar"
    )

    def __repr__(self) -> str:
        return f"Misdar(misdar_id={self.misdar_id!r})"


class MisdarAttendanceRecord(Base):
    __tablename__ = "misdar_attendance_records"
    __table_args__ = (
        UniqueConstraint("soldier_id", "misdar_id", name="uq_misdar_attendance_soldier_misdar"),
    )

    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.soldier_id", ondelete="RESTRICT"), primary_key=True
    )
    misdar_id: Mapped[int] = mapped_column(
        ForeignKey("misdars.misdar_id", ondelete="RESTRICT"), primary_key=True
    )
    scan_time: Mapped[time] = mapped_column(Time, nullable=False)

    soldier: Mapped["Soldier"] = relationship(back_populates="misdar_attendance_records")
    misdar: Mapped["Misdar"] = relationship(back_populates="attendance_records")

    def __repr__(self) -> str:
        return (
            "MisdarAttendanceRecord("
            f"soldier_id={self.soldier_id!r}, misdar_id={self.misdar_id!r}"
            ")"
        )


from db.models.soldier import Soldier  # noqa: E402

