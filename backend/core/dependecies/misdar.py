from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Repositories.Interfaces.baseRepo import IBaseRepo
from Repositories.Interfaces.indication import ISoldierIndicationRepo
from Repositories.Interfaces.misdar import IMisdarAttendanceRepo
from Repositories.misdar import MisdarAttendanceRepository, MisdarTypeRepository
from Services.Interfaces.misdar import IMisdarService
from Services.misdar import MisdarService
from core.dependecies.indication import get_soldier_indication_repository
from core.dependecies.soldier import get_soldier_repository
from db.db import get_db
from db.models.misdar import MisdarType
from Repositories.Interfaces.soldier import ISoldierRepo


async def get_misdar_attendance_repository(db: AsyncSession = Depends(get_db)) -> IMisdarAttendanceRepo:
    return MisdarAttendanceRepository(db)


async def get_misdar_type_repository(db: AsyncSession = Depends(get_db)) -> MisdarTypeRepository:
    return MisdarTypeRepository(db)


async def get_misdar_attendance_service(
    attendance_repository: IMisdarAttendanceRepo = Depends(get_misdar_attendance_repository),
    type_repository: IBaseRepo[MisdarType] = Depends(get_misdar_type_repository),
    indication_repository: ISoldierIndicationRepo = Depends(get_soldier_indication_repository),
    soldier_repository: ISoldierRepo = Depends(get_soldier_repository)) -> IMisdarService:
    return MisdarService(attendance_repository, type_repository, indication_repository, soldier_repository)
