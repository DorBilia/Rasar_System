from calendar import monthrange
from datetime import date
from typing import Optional, Sequence

from sqlalchemy import select, func, Row

from db.models.misdar import MisdarAttendance, MisdarType, MisdarTypeDays
from Repositories.AbstractRepo import AbstractRepo
from sqlalchemy.ext.asyncio import AsyncSession
from Repositories.Interfaces.misdar import IMisdarAttendanceRepo


class MisdarAttendanceRepository(AbstractRepo[MisdarAttendance], IMisdarAttendanceRepo):
    def __init__(self, db: AsyncSession):
        super().__init__(db, MisdarAttendance)

    async def get_filtered(
            self,
            misdar_date: Optional[date] = None,
            misdar_type: Optional[int] = None) -> Sequence[Row]:

        query = select(
            MisdarAttendance.misdar_date,
            MisdarAttendance.misdar_type,
            func.count().label('scan_count')
        )

        if misdar_date is not None:
            query = query.where(MisdarAttendance.misdar_date == misdar_date)

        if misdar_type is not None:
            query = query.where(MisdarAttendance.misdar_type == misdar_type)

        query = query.group_by(
            MisdarAttendance.misdar_date,
            MisdarAttendance.misdar_type
        )

        result = await self.db.execute(query)

        return result.all()

    async def exists_for_soldier(self, soldier_id: int, misdar_date: date, misdar_type: int) -> bool:
        """Used for duplicate checking"""
        query = select(MisdarAttendance.id).where(
            MisdarAttendance.soldier_id == soldier_id,
            MisdarAttendance.misdar_date == misdar_date,
            MisdarAttendance.misdar_type == misdar_type,
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_absence_report(self) -> Sequence[MisdarAttendance]:
        pass

    async def get_misdar_attendances_for_month(self, soldier_id: int, date: date) -> Sequence[MisdarAttendance]:
        month_start = date.replace(day=1)
        month_end = date.replace(day=monthrange(date.year, date.month)[1])

        query = select(MisdarAttendance).where(
            MisdarAttendance.soldier_id == soldier_id,
            MisdarAttendance.misdar_date.between(month_start, month_end))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_misdar_days(self) -> Sequence[MisdarTypeDays]:
        query = select(MisdarTypeDays)
        result = await self.db.execute(query)
        return result.scalars().all()


class MisdarTypeRepository(AbstractRepo[MisdarType]):

    def __init__(self, db: AsyncSession):
        super().__init__(db, MisdarType)
