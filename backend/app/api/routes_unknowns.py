from fastapi import APIRouter
from app.dependencies import unknown_gallery_service

router = APIRouter(prefix="/unknowns", tags=["unknowns"])

@router.get("")
def unknowns():
    return {"unknown_captures": unknown_gallery_service.list_recent(50)}