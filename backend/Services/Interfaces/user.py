from abc import ABC, abstractmethod
from typing import Optional

from API.schemas.auth import RegisterRequest, TokenRequest, TokenResponse, UserResponse, AuthCredentials


class IUserService(ABC):

    @abstractmethod
    async def register(self, register: RegisterRequest) -> UserResponse:
        pass

    @abstractmethod
    async def login(self, login: TokenRequest) -> Optional[TokenResponse]:
        pass

    @abstractmethod
    async def refresh(self, refresh_token: str) -> TokenResponse:
        pass

    @abstractmethod
    async def revoke(self, refresh_token: str) -> None:
        pass

    @abstractmethod
    async def authenticate_user(self, creds: AuthCredentials) -> UserResponse:
        pass
