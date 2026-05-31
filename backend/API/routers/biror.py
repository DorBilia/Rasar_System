from typing import List, Sequence

from fastapi import APIRouter, Depends, HTTPException
from fastapi_restful.cbv import cbv
from sqlalchemy.exc import IntegrityError
from starlette import status

from API.schemas.biror import *
from Services.Interfaces.biror import IBirorService, IBirorTypeService
from core.dependencies.biror import get_biror_service, get_biror_type_service

biror_router = APIRouter(prefix="/birors", tags=["Biror"])
biror_type_router = APIRouter(prefix="/biror/types", tags=["BirorTypes"])


@cbv(biror_type_router)
class BirorTypeRouter:
    service: IBirorTypeService = Depends(get_biror_type_service)

    @biror_type_router.get("/", response_model=List[BirorTypeSchema])
    async def get_all(self):
        return await self.service.get_all()

    @biror_type_router.post("/", response_model=BirorTypeSchema, status_code=status.HTTP_201_CREATED)
    async def create(self, request: CreateBirorTypeRequest):
        return await self.service.create(request)

    @biror_type_router.get("/{biror_type_id}", response_model=BirorTypeSchema)
    async def get_by_id(self, biror_type_id: int):
        row = await self.service.get_by_id(biror_type_id)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="biror type not found")
        return row

    @biror_type_router.put("/{biror_type_id}", response_model=BirorTypeSchema)
    async def update(self, biror_type_id: int, request: UpdateBirorTypeRequest):
        row = await self.service.update(biror_type_id, request)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="biror type not found")
        return row

    @biror_type_router.delete("/{biror_type_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(self, biror_type_id: int):
        try:
            success = await self.service.delete(biror_type_id)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="biror type is referenced and cannot be deleted",
            )
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="biror type not found")
        return None


@cbv(biror_router)
class BirorRouter:
    service: IBirorService = Depends(get_biror_service)

    @biror_router.post("/create", response_model=BirorSchema, status_code=status.HTTP_201_CREATED)
    async def create(self, request: CreateBirorRequest):
        return await self.service.create(request)

    @biror_router.get("/result/{biror_result_id}", response_model=Sequence[BirorSchema])
    async def get_by_result(self, biror_result_id: int):
        return await self.service.get_by_result(biror_result_id)

    @biror_router.get("/soldier/{soldier_id}", response_model=Sequence[BirorSchema])
    async def get_for_soldier(self, soldier_id: int):
        return await self.service.get_for_soldier(soldier_id)

    @biror_router.get("/{biror_uuid}", response_model=BirorSchema)
    async def get_by_uuid(self, biror_uuid: str):
        row = await self.service.get_by_uuid(biror_uuid)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="biror not found")
        return row

    @biror_router.put("/{biror_uuid}", response_model=BirorSchema)
    async def update(self, biror_uuid: str, request: UpdateBirorRequest):
        row = await self.service.update(biror_uuid, request)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="biror not found")
        return row

    @biror_router.delete("/{biror_uuid}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(self, biror_uuid: str):
        try:
            success = await self.service.delete(biror_uuid)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="biror is referenced and cannot be deleted",
            )
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="biror not found")
        return None
