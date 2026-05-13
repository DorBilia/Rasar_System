from datetime import date
from typing import Sequence

from sqlalchemy import select

from db.models.misdar import MisdarAttendance, MisdarType
from Repositories.AbstractRepo import AbstractRepo
from sqlalchemy.ext.asyncio import AsyncSession
from Repositories.Interfaces.misdar import IMisdarAttendanceRepo


class MisdarAttendanceRepository(AbstractRepo[MisdarAttendance], IMisdarAttendanceRepo):
    def __init__(self, db: AsyncSession):
        super().__init__(db, MisdarAttendance)

    async def get_by_date_range(self, start_date: date, end_date: date) -> Sequence[MisdarAttendance]:
        query = select(MisdarAttendance).where(MisdarAttendance.misdar_date.between(start_date, end_date))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_misdar_type(self, misdar_type: str) -> Sequence[MisdarAttendance]:
        query = (
            select(MisdarAttendance)
            .join(MisdarAttendance.misdar_type_ref)
            .where(MisdarType.id == misdar_type)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    def get_absence_report(self) -> Sequence[MisdarAttendance]:
        pass


class MisdarTypeRepository(AbstractRepo[MisdarType]):

    def __init__(self, db: AsyncSession):
        super().__init__(db, MisdarType)
