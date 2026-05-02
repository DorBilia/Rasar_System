from __future__ import annotations

from typing import List

from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.Biror import Biror
from db.models.Indication import SoldierIndication
from db.models.Misdar import MisdarAttendance
from db.models.Ptor import Ptor


class Soldier(Base):
    __tablename__ = "soldiers"
    soldier_id: Mapped[int] = mapped_column(primary_key=True, index=True)

    attendances: Mapped[List["MisdarAttendance"]] = relationship(back_populates="soldier")
    indications: Mapped[List["SoldierIndication"]] = relationship(back_populates="soldier")
    ptors: Mapped[List["Ptor"]] = relationship(back_populates="soldier")
    birorim: Mapped[List["Biror"]] = relationship(back_populates="soldier")

