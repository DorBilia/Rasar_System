from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Services.user import UserService
from Services.Interfaces.user import IUserService
from Repositories.user import UserRepository
from Repositories.Interfaces.user import IUserRepo

from db.db import get_db


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> IUserRepo:
    return UserRepository(db)


async def get_user_service(repository: IUserRepo = Depends(get_user_repository)) -> IUserService:
    return UserService(repository)
