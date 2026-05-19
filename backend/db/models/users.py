"""Authentication/authorization models (users and roles)."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from core.enums import RoleNameEnum

__all__ = ["Role", "User"]

if TYPE_CHECKING:
    from db.models.soldier import Soldier


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    role_name: Mapped[RoleNameEnum] = mapped_column(
        SAEnum(RoleNameEnum, native_enum=False), nullable=False
    )
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r})"


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    soldier_id: Mapped[int] = mapped_column(
        ForeignKey("soldiers.id", ondelete="RESTRICT"), primary_key=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)

    soldier: Mapped["Soldier"] = relationship(back_populates="user")
    role: Mapped["Role"] = relationship(back_populates="users")

    def __repr__(self) -> str:
        return f"User(soldier_id={self.soldier_id!r})"