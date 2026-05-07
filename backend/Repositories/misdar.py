from typing import Optional, List
from db.models.misdar import MisdarAttendance, MisdarType
from Repositories.AbstractRepo import AbstractRepo


class MisdarAttendanceRepository(AbstractRepo[MisdarAttendance]):
    def __init__(self):
        super().__init__(MisdarAttendance)


class MisdarTypeRepository(AbstractRepo[MisdarType]):

    def __init__(self):
        super().__init__(MisdarType)
