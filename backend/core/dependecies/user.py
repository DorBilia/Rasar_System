from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Services.user import UserService
from Services.Interfaces.user import IUserService
from Repositories.user import UserRepository
from Repositories.Interfaces.user import IUserRepo
from Repositories.Interfaces.role import IRoleRepo
from Repositories.Interfaces.refresh_token import IRefreshTokenRepo
from Repositories.Interfaces.soldier import ISoldierRepo

from db.db import get_db
from core.dependecies.role import get_role_repository
from core.dependecies.refresh_token import get_refresh_token_repository
from core.dependecies.soldier import get_soldier_repository


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> IUserRepo:
    return UserRepository(db)


async def get_user_service(
    user_repo: IUserRepo = Depends(get_user_repository),
    role_repo: IRoleRepo = Depends(get_role_repository),
    refresh_repo: IRefreshTokenRepo = Depends(get_refresh_token_repository),
    soldier_repo: ISoldierRepo = Depends(get_soldier_repository),
) -> IUserService:
    return UserService(user_repo, role_repo, refresh_repo, soldier_repo)
