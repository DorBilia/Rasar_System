from sqlalchemy import select, update, delete
from typing import Optional, List

from Repositories.abstract_repo import AbstractRepo
from db.models.misdar import MisdarAttendance, MisdarType
from Repositories import abstract_repo


class MisdarAttendanceRepository(AbstractRepo[MisdarAttendance]):
    def __init__(self):
        super().__init__(MisdarAttendance)


class MisdarTypeRepository(AbstractRepo):

    def __init__(self):
        super().__init__(MisdarType)
