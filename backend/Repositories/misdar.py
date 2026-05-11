from db.models.misdar import MisdarAttendance, MisdarType
from Repositories.AbstractRepo import AbstractRepo
from sqlalchemy.ext.asyncio import AsyncSession


class MisdarAttendanceRepository(AbstractRepo[MisdarAttendance]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)


class MisdarTypeRepository(AbstractRepo[MisdarType]):

    def __init__(self, db: AsyncSession):
        super().__init__(MisdarType)
