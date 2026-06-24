from pathlib import Path
from fastapi import HTTPException, APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix="/images", tags=["Images"])

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")


@router.get("/{image_id}")
def get_image(image_id: str):
    current_directory = Path(__file__).parent

    for ext in SUPPORTED_EXTENSIONS:
        target_file = current_directory / f"{image_id}{ext}"
        if target_file.is_file():
            return FileResponse(target_file)

    raise HTTPException(
        status_code=404, detail=f"Image with ID '{image_id}' not found."
    )
