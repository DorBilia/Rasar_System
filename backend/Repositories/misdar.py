from calendar import monthrange
from datetime import date, time
from typing import Optional, Sequence

from sqlalchemy import select, func, Row, delete
from sqlalchemy.orm import selectinload

from db.models.misdar import MisdarAttendance, MisdarType, MisdarTypeDays
from Repositories.AbstractRepo import AbstractRepo
from sqlalchemy.ext.asyncio import AsyncSession
from Repositories.Interfaces.misdar import IMisdarAttendanceRepo, IMisdarTypeRepo
from core.enums import DayOfWeek
from enums import MisdarNameEnum


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


class MisdarTypeRepository(AbstractRepo[MisdarType], IMisdarTypeRepo):

    def __init__(self, db: AsyncSession):
        super().__init__(db, MisdarType)

    async def get_all_with_days(self) -> Sequence[MisdarType]:
        query = select(MisdarType).options(selectinload(MisdarType.misdar_days))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id_with_days(self, entity_id: int) -> Optional[MisdarType]:
        query = (
            select(MisdarType)
            .where(MisdarType.id == entity_id)
            .options(selectinload(MisdarType.misdar_days))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_with_days(
            self,
            *,
            misdar_name,
            misdar_time,
            misdar_length,
            misdar_days: list[DayOfWeek],
    ) -> MisdarType:
        new_entity = MisdarType(
            misdar_name=misdar_name,
            misdar_time=misdar_time,
            misdar_length=misdar_length,
        )
        self.db.add(new_entity)
        await self.db.flush()

        days_rows = [MisdarTypeDays(misdar_type=new_entity.id, misdar_day=day) for day in misdar_days]
        self.db.add_all(days_rows)
        await self.db.commit()

        created = await self.get_by_id_with_days(new_entity.id)
        assert created is not None
        return created

    async def update_with_days(
            self,
            entity_id: int,
            misdar_name: Optional[MisdarNameEnum] = None,
            misdar_time: Optional[time] = None,
            misdar_length: Optional[float] = None,
            misdar_days: Optional[list[DayOfWeek]] = None) -> Optional[MisdarType]:

        updates = {"misdar_name": misdar_name,
                   "misdar_time": misdar_time,
                   "misdar_length": misdar_length, }
        row = await self.update(entity_id, **updates)
        if row is None:
            return None

        if misdar_days is not None:
            await self.db.execute(delete(MisdarTypeDays).where(MisdarTypeDays.misdar_type == entity_id))
            self.db.add_all([MisdarTypeDays(misdar_type=entity_id, misdar_day=day) for day in misdar_days])

        await self.db.commit()
        return await self.get_by_id_with_days(entity_id)
