from base_repo import IBaseRepo
from db.models.ptor import MedicalPtor, BeardStatement
from typing import Sequence
from abc import abstractmethod


class IMedicalPtorRepo(IBaseRepo[MedicalPtor]):

    @abstractmethod
    async def get_by_ptor_type(self, ptor_type: int) -> Sequence[MedicalPtor]:
        # Return a complete ptor + soldier information
        pass


class IBeardStatementRepo(IBaseRepo[BeardStatement]):

    @abstractmethod
    async def get_by_statement_type(self, statement_type: int) -> Sequence[BeardStatement]:
        pass
