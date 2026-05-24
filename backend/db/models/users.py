from __future__ import annotations

from datetime import date
from typing import List

from sqlalchemy import Boolean, Date, Enum as SAEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from core.enums import RoleNameEnum

__all__ = ["User"]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    uuid: Mapped[str] = mapped_column(String(36), nullable=False, unique=True, primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleNameEnum] = mapped_column(SAEnum(RoleNameEnum, native_enum=False), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(email={self.email!r})"
