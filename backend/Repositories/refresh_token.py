from datetime import datetime
from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.refresh_token import RefreshToken
from Repositories.Interfaces.refresh_token import IRefreshTokenRepo
from Repositories.AbstractRepo import AbstractRepo


class RefreshTokenRepository(AbstractRepo[RefreshToken], IRefreshTokenRepo):
    def __init__(self, db: AsyncSession):
        super().__init__(db, RefreshToken)

    async def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        q = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        r = await self.db.execute(q)
        return r.scalar_one_or_none()

    async def delete_by_hash(self, token_hash: str) -> None:
        await self.db.execute(delete(RefreshToken).where(RefreshToken.token_hash == token_hash))
        await self.db.commit()
