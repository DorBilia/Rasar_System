from datetime import date

from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.soldier import Soldier, Doh1
from typing import Sequence, Optional, List
from abc import abstractmethod


class ISoldierRepo(IBaseRepo[Soldier]):

    @abstractmethod
    async def get_doh1_on_date(self, soldier_id: int, doh1_date: date) -> Optional[Doh1]:
        pass

    @abstractmethod
    async def get_all_filtered(
            self,
            unit: Optional[int] = None,
            branch: Optional[int] = None,
            section: Optional[int] = None,
            rank: Optional[str] = None,
            discharge_date: Optional[date] = None,
            service_type: Optional[str] = None,
            phone_number: Optional[str] = None,
            indication_type: Optional[int] = None,
            search_term: Optional[str] = None,
            limit: int = 50) -> Sequence[Soldier]:
        pass

    @abstractmethod
    async def get_doh1_on_month(self, soldier_id: int, date: date) -> Sequence[Doh1]:
        pass
