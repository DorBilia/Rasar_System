from datetime import date
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Date, Text
from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.Soldier import Soldier


class BirorType(Base):
    __tablename__ = "biror_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255))

    birorim: Mapped[List["Biror"]] = relationship(back_populates="biror_type")


class Biror(Base):
    __tablename__ = "birorim"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    soldier_id: Mapped[int] = mapped_column(ForeignKey("soldier.id"), index=True)
    biror_type_id: Mapped[int] = mapped_column(ForeignKey("bir_types.id"))
    date: Mapped[date] = mapped_column(Date)
    description: Mapped[Optional[str]] = mapped_column(Text)
    result: Mapped[Optional[str]] = mapped_column(Text)

    soldier: Mapped["Soldier"] = relationship(back_populates="birorim")
    biror_type: Mapped["BirorType"] = relationship(back_populates="birorim")