from sqlalchemy import select
from typing import Optional, Sequence
from db.models.soldier import Soldier
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.soldier import ISoldierRepo
from sqlalchemy.ext.asyncio import AsyncSession


class SoldierRepository(AbstractRepo[Soldier], ISoldierRepo):

    def __init__(self, db: AsyncSession):
        super().__init__(db, Soldier)

    async def get_all_filtered(
            self,
            unit: Optional[int] = None,
            branch: Optional[int] = None,
            department: Optional[int] = None,
            rank: Optional[str] = None,
            discharge_date: Optional[str] = None,
            service_type: Optional[str] = None,
            phone_number: Optional[str] = None,
            indication_type: Optional[str] = None,
            search_term: Optional[str] = None,  # could be name or id
            limit: int = 50) -> Sequence[Soldier]:

        query = select(Soldier).where(Soldier.isActive)

        query_map = {unit: Soldier.unit == unit,
                     branch: Soldier.branch == branch,
                     department: Soldier.department == department,
                     rank: Soldier.rank == rank,
                     discharge_date: Soldier.discharge_date == discharge_date,
                     service_type: Soldier.service_type == service_type,
                     phone_number: Soldier.phone_number == phone_number,
                     indication_type: Soldier.indications == indication_type}

        for param, condition in query_map.items():
            if param is not None:
                query = query.where(condition)

        if search_term:
            if search_term.isdecimal():
                soldier_id = int(search_term)
                query = query.where(Soldier.id.ilike(soldier_id))
            else:
                query = query.where(
                    Soldier.first_name.ilike(f"%{search_term}%") |
                    Soldier.last_name.ilike(f"%{search_term}%"))

        query = query.limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
