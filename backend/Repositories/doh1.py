from calendar import monthrange
from datetime import date
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.soldier import Doh1
from Repositories.AbstractRepo import AbstractRepo
from Repositories.Interfaces.doh1 import IDoh1Repo


class Doh1Repository(AbstractRepo[Doh1], IDoh1Repo):

    def __init__(self, db: AsyncSession):
        super().__init__(db, Doh1)

    async def get_doh1_on_date(self, soldier_id: int, doh1_date: date) -> Optional[Doh1]:
        query = select(Doh1).where(
            Doh1.soldier_id == soldier_id,
            Doh1.doh1_date == doh1_date)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_doh1_on_month(self, soldier_id: int, selected_date: date) -> Sequence[Doh1]:
        month_start = selected_date.replace(day=1)
        month_end = selected_date.replace(day=monthrange(selected_date.year, selected_date.month)[1])

        query = select(Doh1).where(
            Doh1.soldier_id == soldier_id,
            Doh1.doh1_date.between(month_start, month_end))
        result = await self.db.execute(query)
        return result.scalars().all()
