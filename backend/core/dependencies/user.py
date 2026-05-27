from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Services.user import UserService
from Services.Interfaces.user import IUserService
from Repositories.user import UserRepository
from Repositories.Interfaces.user import IUserRepo
from Repositories.Interfaces.refresh_token import IRefreshTokenRepo

from db.db import get_db
from .refresh_token import get_refresh_token_repository

async def get_user_repository(db: AsyncSession = Depends(get_db)) -> IUserRepo:
    return UserRepository(db)


async def get_user_service(
    user_repo: IUserRepo = Depends(get_user_repository),
    refresh_repo: IRefreshTokenRepo = Depends(get_refresh_token_repository),
) -> IUserService:
    return UserService(user_repo, refresh_repo)
