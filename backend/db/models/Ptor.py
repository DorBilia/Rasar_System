from datetime import date
from typing import List
from sqlalchemy import ForeignKey, String, Date
from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.Soldier import Soldier


class PtorType(Base):
    __tablename__ = "ptor_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))

    ptors: Mapped[List["Ptor"]] = relationship(back_populates="ptor_type")


class Ptor(Base):
    __tablename__ = "ptorim"

    id: Mapped[int] = mapped_column(primary_key=True)
    soldier_id: Mapped[int] = mapped_column(ForeignKey("soldier.id"))
    ptor_id: Mapped[int] = mapped_column(ForeignKey("ptor_types.id"))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)

    soldier: Mapped["Soldier"] = relationship(back_populates="ptors")
    ptor_type: Mapped["PtorType"] = relationship(back_populates="ptors")