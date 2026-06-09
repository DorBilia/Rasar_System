from abc import ABC, abstractmethod
from typing import Optional

from API.schemas.admin import AdminCreateUserRequest, AdminUpdateUserRequest, AdminUserResponse
from API.schemas.auth import AuthRequest, AuthRequest, TokenResponse, UserResponse, AuthCredentials


class IUserService(ABC):

    @abstractmethod
    async def register(self, register: AuthRequest) -> UserResponse:
        pass

    @abstractmethod
    async def login(self, login: AuthRequest) -> Optional[TokenResponse]:
        pass

    @abstractmethod
    async def refresh(self, refresh_token: str, signed_csrf_token: str) -> TokenResponse:
        pass

    @abstractmethod
    async def revoke(self, refresh_token: str) -> None:
        pass

    @abstractmethod
    async def authenticate_user(self, creds: AuthCredentials) -> UserResponse:
        pass

    @abstractmethod
    async def verify_admin(self, creds: AuthCredentials) -> bool:
        pass

    @abstractmethod
    async def get_users(self) -> list[AdminUserResponse]:
        pass

    @abstractmethod
    async def create_user(self, request: AdminCreateUserRequest) -> AdminUserResponse:
        pass

    @abstractmethod
    async def update_user(
            self,
            user_uuid: str,
            request: AdminUpdateUserRequest,
            actor_uuid: str,
    ) -> AdminUserResponse:
        pass

    @abstractmethod
    async def delete_user(self, user_uuid: str, actor_uuid: str) -> bool:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[AdminUserResponse]:
        pass
