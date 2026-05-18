from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_restful.cbv import cbv
from typing import Sequence

from sqlalchemy.exc import IntegrityError

from API.schemas.soldier import BaseSoldier, FilterSoldiersRequest, FullSoldier, UpdateSoldierRequest
from Services.Interfaces.soldier import ISoldierService

from core.dependecies.soldier import get_soldier_service

router = APIRouter(prefix="/soldiers", tags=["Soldiers"])


@cbv(router)
class SoldierRouter:
    service: ISoldierService = Depends(get_soldier_service)

    @router.post("/filter", response_model=Sequence[BaseSoldier])
    async def get_soldiers(self, request: FilterSoldiersRequest):
        return await self.service.get_all_filtered(request)

    @router.post("/create", response_model=FullSoldier)
    async def create(self, request: FullSoldier):
        try:
            return await self.service.create(request)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="The soldier id you entered already exists")

    @router.get("/{soldier_id}", response_model=FullSoldier)
    async def get_soldier_by_id(self, soldier_id: int):
        soldier = await self.service.get_by_id(soldier_id)
        if not soldier:
            raise HTTPException(status_code=400, detail="Soldier not found")
        return soldier

    @router.patch("/{soldier_id}", response_model=BaseSoldier)
    async def update_soldier_indication(self, soldier_id: int, update_data: UpdateSoldierRequest) -> BaseSoldier:
        updated_soldier = await self.service.update_soldier(soldier_id, update_data)
        if not updated_soldier:
            raise HTTPException(status_code=404, detail="Update failed")
        return updated_soldier

    @router.delete("/{soldier_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_soldier(self, soldier_id: int):
        success = await self.service.delete_soldier(soldier_id)
        if not success:
            raise HTTPException(status_code=404, detail="Soldier not found")
        return None
