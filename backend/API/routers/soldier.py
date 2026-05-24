from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_restful.cbv import cbv
from typing import Sequence

from sqlalchemy.exc import IntegrityError

from API.schemas.soldier import MinimalSoldier, FilterSoldiersRequest, FullSoldier, UpdateSoldierRequest, \
    CreateSoldierRequest
from Services.Interfaces.soldier import ISoldierService

from core.dependecies.soldier import get_soldier_service

router = APIRouter(prefix="/soldiers", tags=["Soldiers"])

#TODO: decide whether to search by soldier uuid or soldier id
@cbv(router)
class SoldierRouter:
    service: ISoldierService = Depends(get_soldier_service)

    @router.post("/filter", response_model=Sequence[MinimalSoldier])
    async def get_soldiers(self, request: FilterSoldiersRequest):
        return await self.service.get_all_filtered(request)

    @router.post("/create", response_model=FullSoldier)
    async def create(self, request: CreateSoldierRequest):
        try:
            return await self.service.create(request)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="The soldier id you entered already exists")

    @router.get("/{soldier_uuid}", response_model=FullSoldier)
    async def get_soldier_by_uuid(self, soldier_uuid: str):
        soldier = await self.service.get_by_uuid(soldier_uuid)
        if not soldier:
            raise HTTPException(status_code=404, detail="Soldier not found")
        return soldier

    @router.put("/{soldier_uuid}", response_model=MinimalSoldier)
    async def update_soldier_indication(self, soldier_uuid: str, update_data: UpdateSoldierRequest) -> MinimalSoldier:
        updated_soldier = await self.service.update_soldier(soldier_uuid, update_data)
        if not updated_soldier:
            raise HTTPException(status_code=404, detail="Update failed")
        return updated_soldier

    @router.delete("/{soldier_uuid}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_soldier(self, soldier_uuid: str):
        success = await self.service.delete_soldier(soldier_uuid)
        if not success:
            raise HTTPException(status_code=404, detail="Soldier not found")
        return None
