from base_repo import IBaseRepo
from db.models.ptor import MedicalPtor, MedicalPtorType, BeardStatementType, BeardStatement
from typing import Sequence
from abc import abstractmethod


class IMedicalPtorRepo(IBaseRepo[MedicalPtor]):

    @abstractmethod
    async def get_for_soldier(self, soldier_id: int) -> Sequence[MedicalPtor]:
        pass

