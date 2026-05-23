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

    def __init__(self, repository: ISoldierIndicationRepo, org_repo: IOrganizationIndicationRepo) -> None:
        self._repository = repository
        self.org_repository = org_repo

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

    async def get_all_for_soldier(self, soldier_id: int) -> Sequence[SoldierIndicationWithDescription]:
        indications = await self._repository.get_for_soldier(soldier_id)

        for indication in indications:
            # Add the indication description
            indication.__setattr__('indication_description',
                                   indication.indication_type_ref.indication_description)

            # Add organization id if there is one
            org_id = indication.organization_id
            if org_id is not None:
                org_object = await self.org_repository.get_by_id(org_id)
                if org_object is not None:
                    org_uuid = org_object.uuid
                    indication.__setattr__('organization_uuid', org_uuid)

        return [SoldierIndicationWithDescription.model_validate(i) for i in indications]

    async def create_many(self, requests: List[SoldierIndicationRequest]) -> List[SoldierIndicationResponse]:
        to_add = []
        org_uuid = requests[0].organization_uuid
        org_object = None

        if org_uuid is not None:
            org_object = await self.org_repository.get_by_uuid(org_uuid)
            if org_object is None:
                return []

        for request in requests:

            indication = Indication(
                soldier_id=request.soldier_id, indication_type=request.indication_type, start_date=request.start_date,
                end_date=request.end_date, uuid=str(uuid.uuid4()))

            if org_object is not None:
                indication.organization_id = org_object.id

            to_add.append(indication)

        created = await self._repository.create_many(to_add)

        if org_uuid is not None:
            for ind in created:
                ind.__setattr__('organization_uuid', org_uuid)
        return [SoldierIndicationResponse.model_validate(r) for r in created]


class OrganizationIndicationService(IOrganizationIndicationService):

    def __init__(self, repository: IOrganizationIndicationRepo, soldier_indication_service: ISoldierIndicationService):
        self._repository = repository
        self._soldier_indication_service = soldier_indication_service

    async def get_all(self) -> Sequence[OrganizationIndicationMinimal]:
        org_indications = await self._repository.get_all_with_soldiers()
        result = []
        for ind in org_indications:
            soldier_ids = [ind.soldier_id for ind in ind.indications]

            ind.__setattr__('additional_soldiers', soldier_ids)
            result.append(OrganizationIndicationMinimal.model_validate(ind))

        return result

    async def get_by_uuid(self, indication_uuid: str) -> Optional[OrganizationIndicationResponse]:
        row = await self._repository.get_by_uuid(indication_uuid)
        if row is None:
            return None
        soldier_ids = await self._repository.get_soldier_ids_by_organization_id(row.id)
        return OrganizationIndicationResponse.model_validate(row).model_copy(
            update={"additional_soldiers": list(soldier_ids)})

    async def create(self, request: OrganizationIndicationRequest) -> OrganizationIndicationResponse:
        data = request.model_dump(exclude={"additional_soldiers"})
        data["uuid"] = str(uuid.uuid4())
        created = await self._repository.create(**data)

        soldiers = request.additional_soldiers

        if soldiers is not None:
            # create an indication for each additional soldier

            indications = [SoldierIndicationRequest(
                soldier_id=soldier_id, indication_type=request.indication_type, start_date=request.start_date,
                end_date=request.end_date, organization_uuid=created.uuid)
                for soldier_id in soldiers]

            await self._soldier_indication_service.create_many(indications)

        return OrganizationIndicationResponse.model_validate(created)

    async def get_by_indication_type(self, indication_type: IndicationType) -> Sequence[OrganizationIndicationResponse]:
        pass
