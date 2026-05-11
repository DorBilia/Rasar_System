from db.models.indications import Indication, IndicationType
from Repositories.AbstractRepo import AbstractRepo
from sqlalchemy.ext.asyncio import AsyncSession


class IndicationRepository(AbstractRepo[Indication]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Indication)


class IndicationTypeRepository(AbstractRepo[Indication]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, IndicationType)
