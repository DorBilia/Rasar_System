from abc import ABC, abstractmethod
from typing import Optional

from API.schemas.user import Login, Register, UserResponse


class IUserService(ABC):

    @abstractmethod
    async def register(self, register: Register) -> UserResponse:
        pass

    @abstractmethod
    async def login(self, login: Login) -> Optional[UserResponse]:
        pass
