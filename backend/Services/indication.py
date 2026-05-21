import uuid

from Repositories.Interfaces.baseRepo import IBaseRepo
from Repositories.Interfaces.indication import ISoldierIndicationRepo, IOrganizationIndicationRepo
from Services.Interfaces.indication import *
from db.models import Indication


class IndicationService(IIndicationService):

    def __init__(self, type_repository: IBaseRepo[IndicationType]):
        self.type_repository = type_repository

    async def get_types(self) -> List[IndicationType]:
        result = await self.type_repository.get_all()
        return [IndicationType.model_validate(r) for r in result]


class SoldierIndicationService(ISoldierIndicationService):

    def __init__(self, repository: ISoldierIndicationRepo) -> None:
        self._repository = repository

    async def create(self, request: SoldierIndicationRequest) -> SoldierIndicationResponse:
        data = request.model_dump()
        data["uuid"] = str(uuid.uuid4())
        created = await self._repository.create(**data)
        return SoldierIndicationResponse.model_validate(created)

    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[SoldierIndicationResponse]:
        indications_result = await self._repository.get_by_indication_type(indication_type)
        return [SoldierIndicationResponse.model_validate(r) for r in indications_result]

    async def can_soldier_attend_misdar(self, soldier_id: int, misdar_id: int) -> bool:
        return await self._repository.can_soldier_attend_misdar(soldier_id, misdar_id)

    async def get_by_uuid(self, indication_uuid: str) -> Optional[SoldierIndicationResponse]:
        result = await self._repository.get_by_uuid(indication_uuid)
        if result is None:
            return None
        return SoldierIndicationResponse.model_validate(result)

    async def create_many(self, requests: List[SoldierIndicationRequest]) -> List[SoldierIndicationResponse]:
        to_add = []
        for request in requests:

            indication = Indication(
                soldier_id=request.soldier_id, indication_type=request.indication_type, start_date=request.start_date,
                end_date=request.end_date, uuid= str(uuid.uuid4()))

            org_id = request.organization_id
            if org_id is not None:
                indication.organization_id = org_id

            to_add.append(indication)

        created = await self._repository.create_many(to_add)
        return [SoldierIndicationResponse.model_validate(r) for r in created]


class OrganizationIndicationService(IOrganizationIndicationService):

    def __init__(self, repository: IOrganizationIndicationRepo, soldier_indication_service: ISoldierIndicationService):
        self._repository = repository
        self._soldier_indication_service = soldier_indication_service

    async def get_all(self) -> Sequence[OrganizationIndicationMinimal]:
        rows = await self._repository.get_all_minimal()
        return [
            OrganizationIndicationMinimal(
                uuid=row.uuid,
                type=row.indication_description.value,
                start_date=row.start_date,
                end_date=row.end_date,
                soldiers_affected=row.soldiers_affected,
            )
            for row in rows
        ]

    async def get_by_uuid(self, indication_uuid: str) -> Optional[OrganizationIndicationResponse]:
        row = await self._repository.get_by_uuid(indication_uuid)
        if row is None:
            return None
        soldier_ids = await self._repository.get_soldier_ids_by_organization_id(row.id)
        return OrganizationIndicationResponse.model_validate(row).model_copy(
            update={"additional_soldiers": list(soldier_ids)}
        )

    async def create(self, request: OrganizationIndicationRequest) -> OrganizationIndicationResponse:
        data = request.model_dump(exclude={"additional_soldiers"})
        data["uuid"] = str(uuid.uuid4())
        created = await self._repository.create(**data)

        soldiers = request.additional_soldiers

        if soldiers is not None:
            # create an indication for each additional soldier

            indications = []

            for soldier_id in soldiers: # build indications list for the soldiers
                indication = SoldierIndicationRequest(
                    soldier_id=soldier_id, indication_type=request.indication_type, start_date=request.start_date,
                    end_date=request.end_date, organization_id=created.id)
                indications.append(indication)

            await self._soldier_indication_service.create_many(indications)

        return OrganizationIndicationResponse.model_validate(created)

    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[OrganizationIndicationResponse]:
        pass
