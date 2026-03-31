from app.utils.time_utils import timestamp_str
from app.utils.image_utils import save_image


class UnknownCaptureManager:
    def __init__(self, unknown_dir):
        self.unknown_dir = unknown_dir

    def save_unknown(self, crop, frame_idx, signature=None):
        unknown_id = f"unknown_{timestamp_str()}_{frame_idx}"
        filename = f"{unknown_id}.jpg"
        path = self.unknown_dir / filename
        save_image(path, crop)

        return {
            "unknown_id": unknown_id,
            "file_name": filename,
            "file_path": f"/static/unlabeled_captures/{filename}",
            "assigned_name": None,
            "signature": signature or {},
        }