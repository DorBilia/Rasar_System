from fastapi import APIRouter, HTTPException, status, Depends, UploadFile
from fastapi_restful.cbv import cbv
from typing import Sequence

from sqlalchemy.exc import IntegrityError

from API.schemas.soldier import *
from Services.Interfaces.soldier import ISoldierService

from core.dependencies.soldier import get_soldier_service

soldiers_router = APIRouter(prefix="/soldiers", tags=["Soldiers"])
doh1_router = APIRouter(prefix="/doh1", tags=["Doh1"])


# TODO: decide whether to search by soldier uuid or soldier id
@cbv(soldiers_router)
class SoldierRouter:
    service: ISoldierService = Depends(get_soldier_service)

    @soldiers_router.post("/filter", response_model=FilterSoldiersResponse)
    async def get_soldiers(self, request: FilterSoldiersRequest):
        return await self.service.get_all_filtered(request)

    @soldiers_router.post("/create", response_model=FullSoldier)
    async def create(self, request: CreateSoldierRequest):
        try:
            return await self.service.create(request)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="The soldier id you entered already exists")

    @soldiers_router.get("/{soldier_uuid}", response_model=FullSoldier)
    async def get_soldier_by_uuid(self, soldier_uuid: str):
        soldier = await self.service.get_by_uuid(soldier_uuid)
        if not soldier:
            raise HTTPException(status_code=404, detail="Soldier not found")
        return soldier

    @soldiers_router.put("/{soldier_uuid}", response_model=MinimalSoldier)
    async def update_soldier_indication(self, soldier_uuid: str, update_data: UpdateSoldierRequest) -> MinimalSoldier:
        updated_soldier = await self.service.update_soldier(soldier_uuid, update_data)
        if not updated_soldier:
            raise HTTPException(status_code=404, detail="Update failed")
        return updated_soldier

    @soldiers_router.delete("/{soldier_uuid}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_soldier(self, soldier_uuid: str):
        success = await self.service.delete_soldier(soldier_uuid)
        if not success:
            raise HTTPException(status_code=404, detail="Soldier not found")
        return None


@cbv(doh1_router)
class Doh1Router:
    service: ISoldierService = Depends(get_soldier_service)

    @doh1_router.post("/create", status_code=status.HTTP_201_CREATED)
    async def create(self, request: Doh1Request):
        if not await self.service.add_doh1_manual(request):
            raise HTTPException(status_code=404, detail="Soldier not found")
        return None

    @doh1_router.post("/upload-excel", status_code=status.HTTP_201_CREATED)
    async def upload_excel(self, file: UploadFile):
        file_bytes = await file.read()
        try:
            success = await self.service.handle_doh1_excel(file_bytes)
            if not success:
                raise HTTPException(status_code=500, detail="Upload failed")

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse Excel file: {str(e)}")

