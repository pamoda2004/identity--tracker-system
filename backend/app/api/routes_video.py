import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import BASE_DIR
from app.dependencies import tracking_service

router = APIRouter(prefix="/video", tags=["video"])

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    save_dir = BASE_DIR / "assets" / "input_videos"
    save_dir.mkdir(parents=True, exist_ok=True)
    file_path = save_dir / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"message": "uploaded", "path": str(file_path)}

@router.post("/start")
def start_video(video_path: str | None = None):
    ok = tracking_service.open(video_path)
    if not ok:
        raise HTTPException(status_code=400, detail="Could not open video source")
    return {"message": "video processing started"}

@router.post("/stop")
def stop_video():
    tracking_service.stop()
    return {"message": "video processing stopped"}