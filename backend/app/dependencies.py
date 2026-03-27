from app.config import YOLO_MODEL, MAX_INACTIVE_FRAMES, UNKNOWN_DIR
from app.services.unknown_gallery_service import UnknownGalleryService
from app.services.stream_service import StreamService
from app.services.tracking_service import TrackingService

unknown_gallery_service = UnknownGalleryService()
unknown_gallery_service.unknown_dir = UNKNOWN_DIR

stream_service = StreamService()

tracking_service = TrackingService(
    model_path=YOLO_MODEL,
    max_inactive_frames=MAX_INACTIVE_FRAMES,
    unknown_gallery_service=unknown_gallery_service,
    stream_service=stream_service,
)