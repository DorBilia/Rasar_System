from abc import abstractmethod
from typing import Optional

from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.users import User


class IUserRepo(IBaseRepo[User]):

    @abstractmethod
    async def get_by_soldier_id(self, soldier_id: int) -> Optional[User]:
        pass
