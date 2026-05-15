from abc import ABC, abstractmethod
from typing import Sequence

from db.models.ptor import BeardStatement, MedicalPtor


class IBeardStatementService(ABC):
    @abstractmethod
    async def get_by_statement_type(self, statement_type: int) -> Sequence[BeardStatement]:
        pass


class IMedicalPtorService(ABC):
    @abstractmethod
    async def get_by_ptor_type(self, ptor_type: int) -> Sequence[MedicalPtor]:
        pass
