from typing import Sequence

from db.models.ptor import BeardStatement, MedicalPtor
from Repositories.Interfaces.ptor import IBeardStatementRepo, IMedicalPtorRepo
from Services.Interfaces.ptor import IBeardStatementService, IMedicalPtorService


class BeardStatementService(IBeardStatementService):
    def __init__(self, repository: IBeardStatementRepo) -> None:
        self._repository = repository

    async def get_by_statement_type(self, statement_type: int) -> Sequence[BeardStatement]:
        return await self._repository.get_by_statement_type(statement_type)


class MedicalPtorService(IMedicalPtorService):
    def __init__(self, repository: IMedicalPtorRepo) -> None:
        self._repository = repository

    async def get_by_ptor_type(self, ptor_type: int) -> Sequence[MedicalPtor]:
        return await self._repository.get_by_ptor_type(ptor_type)
