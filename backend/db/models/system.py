"""System-level configuration stored in the database."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base


class SystemVariable(Base):
    __tablename__ = "system_variables"

    id: Mapped[int] = mapped_column(primary_key=True)
    system_variables_description: Mapped[str] = mapped_column(String(255), nullable=False)
    system_variables_value: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"SystemVariable(id={self.id!r})"

