from sqlalchemy import select

from Repositories.Interfaces.ptor import IMedicalPtorRepo, IBeardStatementRepo
from typing import Sequence
from db.models.ptor import MedicalPtor, BeardStatement, BeardStatementType, MedicalPtorType
from Repositories.AbstractRepo import AbstractRepo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class BeardStatementRepo(AbstractRepo[BeardStatement], IBeardStatementRepo):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, BeardStatement)

    async def get_by_statement_type(self, statement_type: int) -> Sequence[BeardStatement]:
        stmt = (select(BeardStatement)
                .where(BeardStatement.beard_statement_type == statement_type)
                .options(selectinload(BeardStatement.soldier)))

        result = await self.db.execute(stmt)
        return result.scalars().all()


class MedicalPtorRepo(AbstractRepo[MedicalPtor], IMedicalPtorRepo):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, BeardStatement)

    async def get_by_ptor_type(self, ptor_type: int) -> Sequence[BeardStatement]:
        stmt = (select(BeardStatement)
                .where(BeardStatement.beard_statement_type == ptor_type)
                .options(selectinload(MedicalPtor.soldier)))

        result = await self.db.execute(stmt)
        return result.scalars().all()


class MedicalPtorTypeRepo(AbstractRepo[MedicalPtorType]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, MedicalPtorTypeRepo)


class BeardStatementTypeRepo(AbstractRepo[BeardStatementType]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, BeardStatementTypeRepo)
