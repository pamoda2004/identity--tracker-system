import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

YOLO_MODEL = str(BASE_DIR / os.getenv("YOLO_MODEL", "weights/yolov8n.pt"))
VIDEO_SOURCE = str(BASE_DIR / os.getenv("VIDEO_SOURCE", "assets/input_videos/sample.mp4"))
OUTPUT_FRAMES_DIR = BASE_DIR / os.getenv("OUTPUT_FRAMES_DIR", "assets/output_frames")
UNKNOWN_DIR = BASE_DIR / os.getenv("UNKNOWN_DIR", "assets/unlabeled_captures")
MATCH_THRESHOLD = float(os.getenv("MATCH_THRESHOLD", "0.70"))
MAX_INACTIVE_FRAMES = int(os.getenv("MAX_INACTIVE_FRAMES", "60"))

OUTPUT_FRAMES_DIR.mkdir(parents=True, exist_ok=True)
UNKNOWN_DIR.mkdir(parents=True, exist_ok=True)
(BASE_DIR / "state").mkdir(parents=True, exist_ok=True)