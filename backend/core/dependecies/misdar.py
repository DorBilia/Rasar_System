from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Repositories.misdar import MisdarAttendanceRepository
from Repositories.Interfaces.misdar import IMisdarAttendanceRepo
from Services.misdar import MisdarAttendanceService
from Services.Interfaces.misdar import IMisdarAttendanceService

from db.db import get_db


async def get_misdar_attendance_repository(db: AsyncSession = Depends(get_db)) -> IMisdarAttendanceRepo:
    return MisdarAttendanceRepository(db)


async def get_misdar_attendance_service(
    repository: IMisdarAttendanceRepo = Depends(get_misdar_attendance_repository),
) -> IMisdarAttendanceService:
    return MisdarAttendanceService(repository)
