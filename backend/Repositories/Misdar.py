from sqlalchemy import select, update, delete
from typing import Optional, List
from db.models.Misdar import MisdarAttendance,Misdar
from Repositories import AbstractRepo


class MisdarAttendanceRepository(AbstractRepo):

    async def create(self, **kwargs) -> MisdarAttendance:
        new_misdarAttendance = MisdarAttendance(
            **kwargs
        )
        self.db.add(new_misdarAttendance)
        await self.db.commit()
        await self.db.refresh(new_misdarAttendance)
        return new_misdarAttendance

    async def get_by_id(self, MisdarAttendance_id: int) -> Optional[MisdarAttendance]:
        result = await self.db.execute(select(MisdarAttendance).where(MisdarAttendance.id == MisdarAttendance_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[MisdarAttendance]:
        result = await self.db.execute(select(MisdarAttendance))
        return result.scalars().all()

    async def get_all_for_soldier(self, soldier_id: int) -> List[MisdarAttendance]:
        result = await self.db.execute(select(MisdarAttendance).where(MisdarAttendance.soldier_id == soldier_id))
        return result.scalars().all()

    async def update(self, MisdarAttendance_id: int, **updates) -> Optional[MisdarAttendance]:
        query = (
            update(MisdarAttendance)
            .where(MisdarAttendance.id == MisdarAttendance_id)
            .values(**updates)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(MisdarAttendance_id)

    async def delete(self, MisdarAttendance_id: int) -> bool:
        query = delete(MisdarAttendance).where(MisdarAttendance.id == MisdarAttendance_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0


class MisdarRepository(AbstractRepo):

    async def create(self, description: str) -> Misdar:
        new_type = Misdar(description=description)
        self.db.add(new_type)
        await self.db.commit()
        await self.db.refresh(new_type)
        return new_type

    async def get_by_id(self, misdar_id: int) -> Optional[Misdar]:
        result = await self.db.execute(
            select(Misdar).where(Misdar.id == misdar_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Misdar]:
        result = await self.db.execute(select(Misdar))
        return result.scalars().all()

    async def update(self, misdar_id: int, description: str) -> Optional[Misdar]:
        query = (
            update(Misdar)
            .where(Misdar.id == misdar_id)
            .values(description=description)
            .execution_options(synchronize_session="evaluate")
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(misdar_id)

    async def delete(self, misdar_id: int) -> bool:
        query = delete(Misdar).where(Misdar.id == misdar_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
