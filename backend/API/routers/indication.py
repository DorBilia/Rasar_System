from fastapi import APIRouter, Depends, HTTPException
from fastapi_restful.cbv import cbv
from starlette import status

from Services.Interfaces.indication import *
from core.dependecies.indication import get_soldier_indication_service, get_organization_indication_service, \
    get_indication_service
from API.schemas.indication import *

indication_router = APIRouter(prefix="/indications", tags=["Indications"])
soldier_router = APIRouter(prefix="/indications/soldier", tags=["IndicationsSoldier"])
organization_router = APIRouter(prefix="/indications/organization", tags=["IndicationsOrganization"])


@cbv(indication_router)
class IndicationRouter:
    service: IIndicationService = Depends(get_indication_service)

    @indication_router.get("/types", response_model=List[IndicationType])
    async def get_types(self):
        return await self.service.get_types()


@cbv(soldier_router)
class IndicationSoldierRouter:
    service: ISoldierIndicationService = Depends(get_soldier_indication_service)

    @soldier_router.post("/create", response_model=SoldierIndicationResponse)
    async def create(self, request: SoldierIndicationRequest):
        result = await self.service.create(request)
        if result is None:
            raise HTTPException(status_code=500, detail="somthing went wrong")
        return result

    # TODO: change this to search by id (int) or maybe use the uuid method on types
    @soldier_router.get("/{indication_uuid}", response_model=SoldierIndicationResponse)
    async def get_by_indication_uuid(self, indication_uuid: str):
        result = await self.service.get_by_uuid(indication_uuid)
        if result is None:
            raise HTTPException(status_code=404, detail="indication not found")
        return result

    @soldier_router.get("/all/{soldier_id}", response_model=List[SoldierIndicationWithDescription])
    async def get_by_soldier_id(self, soldier_id: int):
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
