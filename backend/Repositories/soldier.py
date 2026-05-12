from sqlalchemy import select, update, delete
from typing import Optional, Sequence
from db.models.soldier import Soldier
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.soldier import ISoldierRepo
from sqlalchemy.ext.asyncio import AsyncSession


class SoldierRepository(AbstractRepo[Soldier], ISoldierRepo):

    def __init__(self, db: AsyncSession):
        super().__init__(db, Soldier)

    async def get_by_unit(self, unit_id: str) -> Sequence[Soldier]:
        stmt = select(Soldier).where(Soldier.unit == unit_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_branch(self, branch: str) -> Sequence[Soldier]:
        stmt = select(Soldier).where(Soldier.branch == branch)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_department(self, department: str) -> Sequence[Soldier]:
        stmt = select(Soldier).where(Soldier.department == department)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_rank(self, rank: str) -> Sequence[Soldier]:
        stmt = select(Soldier).where(Soldier.rank == rank)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_discharge_date(self, discharge_date: str) -> Sequence[Soldier]:
        stmt = select(Soldier).where(Soldier.discharge_date == discharge_date)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_service_type(self, service_type: str) -> Sequence[Soldier]:
        stmt = select(Soldier).where(Soldier.service_type == service_type)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_phone_number(self, phone_number: str) -> Sequence[Soldier]:
        stmt = select(Soldier).where(Soldier.phone_number == phone_number)
        result = await self.db.execute(stmt)
        return result.scalars().all()
