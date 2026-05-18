from datetime import date

from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.soldier import Soldier, Doh1
from typing import Sequence, Optional, List
from abc import abstractmethod


class ISoldierRepo(IBaseRepo[Soldier]):

    @abstractmethod
    async def get_all_filtered(
            self,
            unit: Optional[str] = None,
            branch: Optional[str] = None,
            section: Optional[str] = None,
            rank: Optional[str] = None,
            discharge_date: Optional[date] = None,
            service_type: Optional[str] = None,
            phone_number: Optional[str] = None,
            indication_type: Optional[str] = None,
            search_term: Optional[str] = None,
            limit: int = 50) -> Sequence[Soldier]:
        pass
