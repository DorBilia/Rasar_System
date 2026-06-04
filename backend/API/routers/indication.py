from fastapi import APIRouter, Depends, HTTPException
from fastapi_restful.cbv import cbv
from starlette import status
from sqlalchemy.exc import IntegrityError

from Services.Interfaces.indication import *
from core.dependencies.indication import get_soldier_indication_service, get_organization_indication_service, \
    get_indication_service
from API.schemas.indication import *
from Services.indication import IndicationTypeNotFoundError, MisdarTypeIdsNotFoundError

indication_router = APIRouter(prefix="/indications", tags=["Indications"])
soldier_router = APIRouter(prefix="/indications/soldier", tags=["IndicationsSoldier"])
organization_router = APIRouter(prefix="/indications/organization", tags=["IndicationsOrganization"])


@cbv(indication_router)
class IndicationRouter:
    service: IIndicationService = Depends(get_indication_service)

    @indication_router.get("/types", response_model=List[IndicationTypeSchema])
    async def get_types(self):
        return await self.service.get_types()

    @indication_router.post("/types", response_model=IndicationTypeSchema, status_code=status.HTTP_201_CREATED)
    async def create_type(self, request: CreateIndicationTypeRequest):
        try:
            return await self.service.create_type(request)
        except MisdarTypeIdsNotFoundError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="One or more misdar types not found")
        except IndicationTypeNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="indication type not found")

    @indication_router.get("/types/{indication_type_id}", response_model=IndicationTypeSchema)
    async def get_type(self, indication_type_id: int):
        row = await self.service.get_type_by_id(indication_type_id)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="indication type not found")
        return row

    @indication_router.put("/types/{indication_type_id}", response_model=IndicationTypeSchema)
    async def update_type(self, indication_type_id: int, request: UpdateIndicationTypeRequest):
        row = await self.service.update_type(indication_type_id, request)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="indication type not found")
        return row

    @indication_router.delete("/types/{indication_type_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_type(self, indication_type_id: int):
        try:
            success = await self.service.delete_type(indication_type_id)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="indication type is referenced and cannot be deleted")

        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="indication type not found")
        return None


@cbv(soldier_router)
class IndicationSoldierRouter:
    service: ISoldierIndicationService = Depends(get_soldier_indication_service)

    @soldier_router.post("/create", response_model=SoldierIndicationResponse)
    async def create(self, request: SoldierIndicationRequest):
        result = await self.service.create(request)
        if result is None:
            raise HTTPException(status_code=500, detail="somthing went wrong")
        return result

    @soldier_router.get("/{indication_uuid}", response_model=SoldierIndicationResponse)
    async def get_by_indication_uuid(self, indication_uuid: str):
        result = await self.service.get_by_uuid(indication_uuid)
        if result is None:
            raise HTTPException(status_code=404, detail="indication not found")
        return result

    @soldier_router.get("/all/{soldier_id}", response_model=List[SoldierIndicationWithDescription])
    async def get_by_soldier_id(self, soldier_id: int):
        """The frontend will classify every indication as active/historical"""
        result = await self.service.get_all_for_soldier(soldier_id)
        return result

    @soldier_router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(self, uuid: str):
        success = await self.service.delete(uuid)
        if not success:
            raise HTTPException(status_code=404, detail="Soldier not found")
        return None


@cbv(organization_router)
class OrganizationSoldierRouter:
    service: IOrganizationIndicationService = Depends(get_organization_indication_service)

    @organization_router.post("/create", response_model=OrganizationIndicationResponse)
    async def create(self, request: OrganizationIndicationRequest):
        result = await self.service.create(request)
        if result is None:
            raise HTTPException(status_code=500, detail="somthing went wrong")
        return result

    @organization_router.get("/", response_model=List[OrganizationIndicationMinimal])
    async def get_all(self):
        return await self.service.get_all()

    @organization_router.get("/{uuid}", response_model=OrganizationIndicationResponse)
    async def get_by_uuid(self, uuid: str):
        result = await self.service.get_by_uuid(uuid)
        if result is None:
            raise HTTPException(status_code=404, detail="Organization indication not found")
        return result

    @organization_router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(self, uuid: str):
        success = await self.service.delete(uuid)
        if not success:
            raise HTTPException(status_code=404, detail="Soldier not found")
        return None
