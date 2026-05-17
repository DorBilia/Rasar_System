import uuid
from Repositories.Interfaces.baseRepo import IBaseRepo
from Repositories.Interfaces.indication import ISoldierIndicationRepo, IOrganizationIndicationRepo
from Services.Interfaces.indication import *


class IndicationService(IIndicationService):

    def __init__(self, type_repository: IBaseRepo[IndicationType]):
        self.type_repository = type_repository

    async def get_types(self) -> List[IndicationType]:
        return await self.type_repository.get_all()


class SoldierIndicationService(ISoldierIndicationService):

    def __init__(self, repository: ISoldierIndicationRepo) -> None:
        self._repository = repository

    async def create(self, request: SoldierIndicationRequest) -> SoldierIndicationResponse:
        data = request.model_dump()
        data.setdefault("id", int(uuid.uuid4()))
        created = await self._repository.create(**data)
        return SoldierIndicationResponse.model_validate(created)

    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[Indication]:  # fix this
        return await self._repository.get_by_indication_type(indication_type)

    async def can_soldier_attend_misdar(self, soldier_id: int, misdar_id: int) -> bool:
        return await self._repository.can_soldier_attend_misdar(soldier_id, misdar_id)

    async def get_by_id(self, id: int) -> SoldierIndicationResponse:
        pass


class OrganizationIndicationService(IOrganizationIndicationService):

    def __init__(self, repository: IOrganizationIndicationRepo) -> None:
        self._repository = repository

    async def get_all(self) -> Sequence[OrganizationIndicationMinimal]:
        pass

    async def get_by_id(self, id: int) -> Sequence[OrganizationIndicationResponse]:
        pass

    async def create(self, request: OrganizationIndicationRequest) -> OrganizationIndicationResponse:
        data = request.model_dump()
        data.setdefault("id", int(uuid.uuid4()))
        created = await self._repository.create(**data)
        return OrganizationIndicationResponse.model_validate(created)

    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[OrganizationIndicationResponse]:
        pass
