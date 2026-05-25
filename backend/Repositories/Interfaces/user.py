from abc import abstractmethod
from typing import Optional

from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.users import User


class IUserRepo(IBaseRepo[User]):

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def count_users(self) -> int:
        pass
