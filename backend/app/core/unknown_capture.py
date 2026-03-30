from app.utils.time_utils import timestamp_str
from app.utils.image_utils import save_image

class UnknownCaptureManager:
    def __init__(self, unknown_dir):
        self.unknown_dir = unknown_dir

    def save_unknown(self, crop, frame_idx):
        filename = f"{timestamp_str()}_unknown_{frame_idx}.jpg"
        path = self.unknown_dir / filename
        save_image(path, crop)
        return {
            "file_name": filename,
            "file_path": f"/static/unlabeled_captures/{filename}",
        }