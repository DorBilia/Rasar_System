from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Repositories.Interfaces.baseRepo import IBaseRepo
from Repositories.misdar import MisdarAttendanceRepository, MisdarTypeRepository
from Repositories.Interfaces.misdar import IMisdarAttendanceRepo
from Services.misdar import MisdarAttendanceService
from Services.Interfaces.misdar import IMisdarService
from db.models.misdar import MisdarType
from db.db import get_db


async def get_misdar_attendance_repository(db: AsyncSession = Depends(get_db)) -> IMisdarAttendanceRepo:
    return MisdarAttendanceRepository(db)


async def get_misdar_type_repository(db: AsyncSession = Depends(get_db)):
    return MisdarTypeRepository(db)


async def get_misdar_attendance_service(
        attendance_repository: IMisdarAttendanceRepo = Depends(get_misdar_attendance_repository),
        type_repository: IBaseRepo[MisdarType] = Depends(get_misdar_type_repository)) -> IMisdarService:
    return MisdarAttendanceService(attendance_repository, type_repository)
