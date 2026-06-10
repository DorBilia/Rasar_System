from sqlalchemy.ext.asyncio import AsyncSession

from db.models.organization import Branch, Section, Unit
from Repositories.AbstractRepo import AbstractRepo


class UnitRepository(AbstractRepo[Unit]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Unit)


class BranchRepository(AbstractRepo[Branch]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Branch)


class SectionRepository(AbstractRepo[Section]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Section)
