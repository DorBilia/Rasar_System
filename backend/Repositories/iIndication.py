from db.models.indications import Indication, IndicationType
from Repositories.AbstractRepo import AbstractRepo


class IndicationRepository(AbstractRepo[Indication]):
    def __init__(self):
        super().__init__(Indication)


class IndicationTypeRepository(AbstractRepo[IndicationType]):
    def __init__(self):
        super().__init__(IndicationType)
