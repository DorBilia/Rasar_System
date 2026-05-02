from datetime import date, time
from typing import List
from sqlalchemy import ForeignKey, String, Date, Time
from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.Soldier import Soldier


class Misdar(Base):
    __tablename__ = "misdarim"

    misdar_id: Mapped[int] = mapped_column(primary_key=True)
    misdar_type: Mapped[str] = mapped_column(String(255))
    misdar_description: Mapped[str] = mapped_column(String(255))
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)

    attendances: Mapped[List["MisdarAttendance"]] = relationship(back_populates="misdar")


class MisdarAttendance(Base):
    __tablename__ = "misdar_attendance"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    soldier_id: Mapped[int] = mapped_column(ForeignKey("soldier.id"), index=True)
    misdar_id: Mapped[int] = mapped_column(ForeignKey("misdarim.misdar_id"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)

    soldier: Mapped["Soldier"] = relationship(back_populates="attendances")
    misdar: Mapped["Misdar"] = relationship(back_populates="attendances")
