from abc import abstractmethod
from typing import Optional
from Repositories.Interfaces.baseRepo import IBaseRepo
from db.models.refresh_token import RefreshToken


class IRefreshTokenRepo(IBaseRepo[RefreshToken]):

    @abstractmethod
    async def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        pass

    @abstractmethod
    async def delete_by_hash(self, token_hash: str) -> None:
        pass
