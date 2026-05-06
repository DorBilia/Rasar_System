from db.models.ptor import MedicalPtor, MedicalPtorType, BeardStatement, BeardStatementType
from AbstractRepo import AbstractRepo


class MedicalPtorRepository(AbstractRepo[MedicalPtor]):
    def __init__(self):
        super().__init__(MedicalPtor)


class MedicalPtorTypeRepository(AbstractRepo[MedicalPtorType]):

    def __init__(self, ):
        super().__init__(MedicalPtorType)
