from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import BASE_DIR
from app.api.routes_health import router as health_router
from app.api.routes_video import router as video_router
from app.api.routes_tracker import router as tracker_router
from app.api.routes_unknowns import router as unknowns_router

app = FastAPI(title="Persistent Identity Tracker V2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

assets_dir = BASE_DIR / "assets"
app.mount("/static", StaticFiles(directory=assets_dir), name="static")

app.include_router(health_router)
app.include_router(video_router)
app.include_router(tracker_router)
app.include_router(unknowns_router)