"""Duties assigned to soldiers (guardings and tasks)."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, List

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from core.enums import GuardingTypeEnum, TaskAssignedByEnum

__all__ = ["Guarding", "GuardingType", "Task", "TaskType"]


class GuardingType(Base):
    __tablename__ = "guarding_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    guarding_description: Mapped[GuardingTypeEnum] = mapped_column(
        SAEnum(GuardingTypeEnum, native_enum=False), nullable=False
    )
    nights_count: Mapped[int] = mapped_column(nullable=False)

    guardings: Mapped[List["Guarding"]] = relationship(back_populates="guarding_type_ref")

    def __repr__(self) -> str:
        return f"GuardingType(id={self.id!r})"


class Guarding(Base):
    __tablename__ = "guardings"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.id", ondelete="RESTRICT"), nullable=False
    )
    guarding_type: Mapped[int] = mapped_column(
        ForeignKey("guarding_types.id", ondelete="RESTRICT"), nullable=False
    )
    guarding_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    guarding_end_date: Mapped[date] = mapped_column(Date, nullable=False)

    soldier: Mapped["Soldier"] = relationship(back_populates="guardings")
    guarding_type_ref: Mapped["GuardingType"] = relationship(back_populates="guardings")

    def __repr__(self) -> str:
        return f"Guarding(id={self.id!r})"


class TaskType(Base):
    __tablename__ = "task_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    task_description: Mapped[str] = mapped_column(String(255), nullable=False)
    assigned_by: Mapped[TaskAssignedByEnum] = mapped_column(
        SAEnum(TaskAssignedByEnum, native_enum=False), nullable=False
    )

    tasks: Mapped[List["Task"]] = relationship(back_populates="task_type_ref")

    def __repr__(self) -> str:
        return f"TaskType(id={self.id!r})"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.id", ondelete="RESTRICT"), nullable=False
    )
    task_type: Mapped[int] = mapped_column(
        ForeignKey("task_types.id", ondelete="RESTRICT"), nullable=False
    )
    task_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    task_end_date: Mapped[date] = mapped_column(Date, nullable=False)

    soldier: Mapped["Soldier"] = relationship(back_populates="tasks")
    task_type_ref: Mapped["TaskType"] = relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"Task(id={self.id!r})"
