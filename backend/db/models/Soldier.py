"""Core soldier records and per-day Doh1 attendance records."""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from db.models.enums import Doh1ValueEnum, RankEnum, ServiceTypeEnum


class Soldier(Base):
    __tablename__ = "soldiers"

    soldier_id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    rank: Mapped[RankEnum] = mapped_column(
        SAEnum(RankEnum, native_enum=False), nullable=False
    )
    framework: Mapped[str] = mapped_column(String(255), nullable=False)
    picture: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    discharge_date: Mapped[date] = mapped_column(Date, nullable=False)
    service_type: Mapped[ServiceTypeEnum] = mapped_column(
        SAEnum(ServiceTypeEnum, native_enum=False), nullable=False
    )
    unit: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)

    doh1_records: Mapped[List["Doh1"]] = relationship(back_populates="soldier")
    medical_ptors: Mapped[List["MedicalPtor"]] = relationship(
        back_populates="soldier"
    )
    beard_statements: Mapped[List["BeardStatement"]] = relationship(
        back_populates="soldier"
    )
    misdars: Mapped[List["Misdar"]] = relationship(back_populates="soldier")
    misdar_attendance_records: Mapped[List["MisdarAttendanceRecord"]] = relationship(
        back_populates="soldier"
    )
    birors: Mapped[List["Biror"]] = relationship(back_populates="soldier")
    indications: Mapped[List["Indication"]] = relationship(back_populates="soldier")
    guardings: Mapped[List["Guarding"]] = relationship(back_populates="soldier")
    tasks: Mapped[List["Task"]] = relationship(back_populates="soldier")
    user: Mapped[Optional["User"]] = relationship(back_populates="soldier")

    def __repr__(self) -> str:
        return f"Soldier(soldier_id={self.soldier_id!r})"


class Doh1(Base):
    __tablename__ = "doh1_records"

    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.soldier_id", ondelete="RESTRICT"), primary_key=True
    )
    doh1_date: Mapped[date] = mapped_column(Date, primary_key=True, nullable=False)
    doh1_value: Mapped[Doh1ValueEnum] = mapped_column(
        SAEnum(Doh1ValueEnum, native_enum=False), nullable=False
    )

    soldier: Mapped["Soldier"] = relationship(back_populates="doh1_records")

    def __repr__(self) -> str:
        return (
            f"Doh1(soldier_id={self.soldier_id!r}, doh1_date={self.doh1_date!r})"
        )

'''
"""Core soldier records and per-day Doh1 attendance records."""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from db.models.enums import Doh1ValueEnum, RankEnum, ServiceTypeEnum


class Soldier(Base):
    __tablename__ = "soldiers"

    soldier_id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    rank: Mapped[RankEnum] = mapped_column(
        SAEnum(RankEnum, native_enum=False), nullable=False
    )
    framework: Mapped[str] = mapped_column(String(255), nullable=False)
    picture: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    discharge_date: Mapped[date] = mapped_column(Date, nullable=False)
    service_type: Mapped[ServiceTypeEnum] = mapped_column(
        SAEnum(ServiceTypeEnum, native_enum=False), nullable=False
    )
    unit: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)

    doh1_records: Mapped[List["Doh1"]] = relationship(back_populates="soldier")
    medical_ptors: Mapped[List["MedicalPtor"]] = relationship(back_populates="soldier")
    beard_statements: Mapped[List["BeardStatement"]] = relationship(
        back_populates="soldier"
    )
    misdars: Mapped[List["Misdar"]] = relationship(back_populates="soldier")
    misdar_attendance_records: Mapped[List["MisdarAttendanceRecord"]] = relationship(
        back_populates="soldier"
    )
    birors: Mapped[List["Biror"]] = relationship(back_populates="soldier")
    indications: Mapped[List["Indication"]] = relationship(back_populates="soldier")
    guardings: Mapped[List["Guarding"]] = relationship(back_populates="soldier")
    tasks: Mapped[List["Task"]] = relationship(back_populates="soldier")
    user: Mapped[Optional["User"]] = relationship(back_populates="soldier")

    def __repr__(self) -> str:
        return f"Soldier(soldier_id={self.soldier_id!r})"


class Doh1(Base):
    __tablename__ = "doh1_records"

    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.soldier_id", ondelete="RESTRICT"), primary_key=True
    )
    doh1_date: Mapped[date] = mapped_column(Date, primary_key=True, nullable=False)
    doh1_value: Mapped[Doh1ValueEnum] = mapped_column(
        SAEnum(Doh1ValueEnum, native_enum=False), nullable=False
    )

    soldier: Mapped["Soldier"] = relationship(back_populates="doh1_records")

    def __repr__(self) -> str:
        return f"Doh1(soldier_id={self.soldier_id!r}, doh1_date={self.doh1_date!r})"

'''
