import httpx
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, Response
from fastapi_restful.cbv import cbv
from core.utils import enforce_size_limit

from sqlalchemy.exc import IntegrityError

from API.schemas.soldier import *
from Services.Interfaces.soldier import ISoldierService
from Services.indication import IndicationTypeNotFoundError

from core.dependencies.soldier import get_soldier_service

soldiers_router = APIRouter(prefix="/soldiers", tags=["Soldiers"])
doh1_router = APIRouter(prefix="/doh1", tags=["Doh1"])

TARGET_BASE_URL = "http://localhost:8001/images"
MAX_IMAGE_BYTES = 5 * 1024 * 1024


@cbv(soldiers_router)
class SoldierRouter:
    service: ISoldierService = Depends(get_soldier_service)

    @soldiers_router.post("/filter", response_model=FilterSoldiersResponse)
    async def get_soldiers(self, request: FilterSoldiersRequest):
        return await self.service.get_all_filtered(request)

    @soldiers_router.post("/create", response_model=FullSoldier)
    async def create(self, request: FullSoldier):
        try:
            return await self.service.create(request)
        except IndicationTypeNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="default indication not found",
            )
        except IntegrityError as e:
            if hasattr(e.orig, "sqlstate") and e.orig.sqlstate == "23503":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Foreign key violation: The referenced record does not exist or is still in use."
                )
            else:
                raise HTTPException(status_code=409, detail="The soldier id you entered already exists")

    @soldiers_router.get("/{soldier_id}", response_model=FullSoldier)
    async def get_soldier_by_id(self, soldier_id: int):
        soldier = await self.service.get_by_id(soldier_id)
        if not soldier:
            raise HTTPException(status_code=404, detail="Soldier not found")
        return soldier

    @soldiers_router.put("/{soldier_id}", response_model=MinimalSoldier)
    async def update_soldier(self, soldier_id: int, update_data: UpdateSoldierRequest):
        updated_soldier = await self.service.update_soldier(soldier_id, update_data)
        if not updated_soldier:
            raise HTTPException(status_code=404, detail="Update failed")
        return updated_soldier

    @soldiers_router.delete("/{soldier_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_soldier(self, soldier_id: int):
        success = await self.service.delete_soldier(soldier_id)
        if not success:
            raise HTTPException(status_code=404, detail="Soldier not found")
        return None


    @soldiers_router.get("/image/{soldier_id}")
    async def fetch_remote_image(self, soldier_id: str):

        if "/" in soldier_id or "\\" in soldier_id or ".." in soldier_id:
            raise HTTPException(status_code=400, detail="Invalid image name format.")

        target_url = f"{TARGET_BASE_URL}/{soldier_id}"

        async with httpx.AsyncClient(follow_redirects=False) as client:
            try:
                async with client.stream("GET", target_url, timeout=5.0) as response:

                    response.raise_for_status()

                    content_type = response.headers.get("Content-Type", "")
                    if not content_type.startswith("image/"):
                        raise HTTPException(status_code=502, detail="Target did not return an image.")

                    content_length = response.headers.get("Content-Length")
                    if content_length and int(content_length) > MAX_IMAGE_BYTES:
                        raise HTTPException(status_code=502, detail="Image header exceeds maximum allowed size.")

                    image_data = bytearray()
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        image_data.extend(chunk)
                        if len(image_data) > MAX_IMAGE_BYTES:
                            raise HTTPException(
                                status_code=502,
                                detail="Image stream exceeded maximum allowed size."
                            )

                    return Response(content=bytes(image_data), media_type=content_type)

            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Remote server returned error: {e.response.status_code}"
                )
            except httpx.RequestError:
                raise HTTPException(
                    status_code=502,
                    detail="Bad Gateway: Could not reach the internal image server."
                )

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
        if not await enforce_size_limit(file):
            raise HTTPException(status_code=400, detail=f"File too large")

        file_bytes = await file.read()
        try:
            success = await self.service.handle_doh1_excel(file_bytes)
            if not success:
                raise HTTPException(status_code=500, detail="Upload failed")

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse Excel file: {str(e)}")

