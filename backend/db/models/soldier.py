"""Core soldier records and per-day Doh1 attendance records."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from core.enums import Doh1ValueEnum, RankEnum, ServiceTypeEnum

__all__ = ["Doh1", "Soldier"]


class Soldier(Base):
    __tablename__ = "soldiers"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)

    rank: Mapped[RankEnum] = mapped_column(SAEnum(RankEnum, native_enum=False), nullable=False)

    picture: Mapped[Optional[str]] = mapped_column(String(1024))  # check about that

    discharge_date: Mapped[date] = mapped_column(Date, nullable=False)
    service_type: Mapped[ServiceTypeEnum] = mapped_column(SAEnum(ServiceTypeEnum, native_enum=False), nullable=False)

    unit: Mapped[int] = mapped_column(ForeignKey("units.id", ondelete="RESTRICT"), nullable=False)
    branch: Mapped[int] = mapped_column(ForeignKey("branches.id", ondelete="RESTRICT"), nullable=False)
    section: Mapped[int] = mapped_column(ForeignKey("sections.id", ondelete="RESTRICT"), nullable=False)

    other_allocations: Mapped[str] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)

    doh1_records: Mapped[List["Doh1"]] = relationship(back_populates="soldier", cascade="all, delete-orphan")
    medical_ptors: Mapped[List["MedicalPtor"]] = relationship(back_populates="soldier", cascade="all, delete-orphan")
    beard_statements: Mapped[List["BeardStatement"]] = relationship(back_populates="soldier",
                                                                    cascade="all, delete-orphan")
    misdar_attendance_records: Mapped[List["MisdarAttendance"]] = relationship(back_populates="soldier",
                                                                               cascade="all, delete-orphan")
    birors: Mapped[List["Biror"]] = relationship(back_populates="soldier", cascade="all, delete-orphan")
    indications: Mapped[List["Indication"]] = relationship(back_populates="soldier", cascade="all, delete-orphan")
    guardings: Mapped[List["Guarding"]] = relationship(back_populates="soldier", cascade="all, delete-orphan")
    tasks: Mapped[List["Task"]] = relationship(back_populates="soldier", cascade="all, delete-orphan")
    unit_ref: Mapped["Unit"] = relationship(back_populates="soldiers", foreign_keys=[unit])
    branch_ref: Mapped["Branch"] = relationship(back_populates="soldiers", foreign_keys=[branch])
    sections_ref: Mapped["Section"] = relationship(back_populates="soldiers", foreign_keys=[section])

    def __repr__(self) -> str:
        return f"Soldier(id={self.id!r})"


class Doh1(Base):
    __tablename__ = "doh1_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    soldier_id: Mapped[int] = mapped_column(ForeignKey("soldiers.id", ondelete="RESTRICT"))
    doh1_date: Mapped[date] = mapped_column(Date, primary_key=True, nullable=False)
    doh1_value: Mapped[Doh1ValueEnum] = mapped_column(SAEnum(Doh1ValueEnum, native_enum=False), nullable=False)

    soldier: Mapped["Soldier"] = relationship(back_populates="doh1_records")

    def __repr__(self) -> str:
        return f"Doh1(soldier_id={self.soldier_id!r}, doh1_date={self.doh1_date!r})"
