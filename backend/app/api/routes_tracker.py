from fastapi import APIRouter
from app.dependencies import tracking_service

router = APIRouter(prefix="/tracker", tags=["tracker"])

@router.get("/frame")
def tracker_frame():
    result = tracking_service.process_next_frame()
    if result is None:
        return {"message": "no more frames or processor not running"}
    return result

@router.get("/active-ids")
def active_ids():
    return {"active_ids": tracking_service.tracker.active_people()}