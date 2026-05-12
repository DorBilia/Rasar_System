from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.soldier import Soldier, Doh1
from typing import Sequence
from abc import abstractmethod


class ISoldierRepo(IBaseRepo[Soldier]):

    @abstractmethod
    async def get_by_unit(self, unit_id: str) -> Sequence[Soldier]:
        pass

    @abstractmethod
    async def get_by_branch(self, branch: str) -> Sequence[Soldier]:
        pass

    @abstractmethod
    async def get_by_department(self, branch: str) -> Sequence[Soldier]:
        pass

    @abstractmethod
    async def get_by_rank(self, rank: str) -> Sequence[Soldier]:
        pass

    @abstractmethod
    async def get_by_discharge_date(self, discharge_date: str) -> Sequence[Soldier]:
        pass

    @abstractmethod
    async def get_by_service_type(self, service_type: str) -> Sequence[Soldier]:
        pass

    @abstractmethod
    async def get_by_phone_number(self, phone_number: str) -> Sequence[Soldier]:
        pass
