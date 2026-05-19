from abc import abstractmethod
from typing import Optional

from Commands.user import LoginCommand, RegisterCommand
from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.users import User


class IUserRepo(IBaseRepo[User]):

    @abstractmethod
    async def register(self, command: RegisterCommand) -> User:
        pass

    @abstractmethod
    async def login(self, command: LoginCommand) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_soldier_id(self, soldier_id: int) -> Optional[User]:
        pass
