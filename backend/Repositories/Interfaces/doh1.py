from datetime import date
from typing import Optional, Sequence
from abc import abstractmethod

from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.soldier import Doh1


class IDoh1Repo(IBaseRepo[Doh1]):

    @abstractmethod
    async def get_doh1_on_date(self, soldier_id: int, doh1_date: date) -> Optional[Doh1]:
        pass

    @abstractmethod
    async def get_doh1_on_month(self, soldier_id: int, selected_date: date) -> Sequence[Doh1]:
        pass
