from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.Soldier import Soldier


class IndicationType(Base):
    __tablename__ = "indication_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))

    indications: Mapped[List["SoldierIndication"]] = relationship(back_populates="indication_type")


class Indication(Base):
    __tablename__ = "soldier_indications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    soldier_id: Mapped[int] = mapped_column(ForeignKey("soldier.id"), index=True)
    indication_id: Mapped[int] = mapped_column(ForeignKey("indication_types.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)

    soldier: Mapped["Soldier"] = relationship(back_populates="indications")
    indication_type: Mapped["IndicationType"] = relationship(back_populates="indications")
