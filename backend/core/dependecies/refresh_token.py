from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Repositories.Interfaces.refresh_token import IRefreshTokenRepo
from Repositories.refresh_token import RefreshTokenRepository
from db.db import get_db


async def get_refresh_token_repository(db: AsyncSession = Depends(get_db)) -> IRefreshTokenRepo:
    return RefreshTokenRepository(db)
