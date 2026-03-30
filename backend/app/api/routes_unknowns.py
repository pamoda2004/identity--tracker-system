from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.dependencies import unknown_gallery_service, named_registry_service

router = APIRouter(prefix="/unknowns", tags=["unknowns"])


class AssignNameRequest(BaseModel):
    unknown_id: str
    name: str


@router.get("")
def unknowns():
    return {"unknown_captures": unknown_gallery_service.list_recent(50)}


@router.post("/assign-name")
def assign_name(payload: AssignNameRequest):
    item = unknown_gallery_service.find_by_unknown_id(payload.unknown_id)
    if not item:
        raise HTTPException(status_code=404, detail="Unknown person not found")

    updated = unknown_gallery_service.assign_name(payload.unknown_id, payload.name)

    named_item = named_registry_service.add_named_person(
        unknown_id=payload.unknown_id,
        name=payload.name,
        signature=updated.get("signature", {}),
        image_path=updated.get("file_path", ""),
    )

    return {
        "message": "name assigned successfully",
        "unknown_person": updated,
        "named_person": named_item,
    }