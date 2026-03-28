from app.config import VIDEO_SOURCE, OUTPUT_FRAMES_DIR, MATCH_THRESHOLD
from app.core.detector import PersonDetector
from app.core.feature_extractor import FeatureExtractor
from app.core.identity_matcher import IdentityMatcher
from app.core.tracker import SimpleTracker
from app.core.unknown_capture import UnknownCaptureManager
from app.core.annotator import FrameAnnotator
from app.utils.image_utils import crop_bbox, center_of_bbox, save_image
from app.core.gait_analyzer import GaitAnalyzer

import cv2
import numpy as np

class TrackingService:

    def _to_python_number(self, value):
        if isinstance(value, (np.float32, np.float64)):
            return float(value)
        if isinstance(value, (np.int32, np.int64)):
            return int(value)
        return value

    def _sanitize_bbox(self, bbox):
        return [float(x) for x in bbox]

    def __init__(self, model_path, max_inactive_frames, unknown_gallery_service, stream_service):
        self.detector = PersonDetector(model_path)
        self.extractor = FeatureExtractor()
        self.matcher = IdentityMatcher(MATCH_THRESHOLD)
        self.tracker = SimpleTracker(max_inactive_frames=max_inactive_frames)
        self.unknown_capture_manager = UnknownCaptureManager(unknown_dir=unknown_gallery_service.unknown_dir if hasattr(unknown_gallery_service, "unknown_dir") else None)
        self.annotator = FrameAnnotator()
        self.unknown_gallery_service = unknown_gallery_service
        self.stream_service = stream_service
        self.cap = None
        self.running = False
        self.video_source = VIDEO_SOURCE
        self.gait_analyzer = GaitAnalyzer()

    def open(self, video_path=None):
        if video_path:
            self.video_source = video_path
        self.cap = cv2.VideoCapture(self.video_source)
        self.running = self.cap.isOpened()
        return self.running

    def stop(self):
        self.running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def process_next_frame(self):
        if not self.running or self.cap is None:
            return None

        ok, frame = self.cap.read()
        if not ok:
            self.stop()
            return None

        self.tracker.frame_index += 1
        detections = self.detector.detect_people(frame)
        output_detections = []

        for det in detections:
            bbox = det["bbox"]
            crop = crop_bbox(frame, bbox)
            features = self.extractor.extract(crop, bbox)
            center = center_of_bbox(bbox)

            # current temporary gait for new detection can be empty at first
            current_gait = {
                "avg_speed": 0.0,
                "direction_x": 0.0,
                "direction_y": 0.0,
                "vertical_oscillation": 0.0,
                "height_variation": 0.0,
                "movement_confidence": 0.0,
            }

            match_id, score = self.matcher.best_match(
                features,
                center,
                self.tracker.people,
                current_gait=current_gait
            ) 

            if match_id is not None:
                self.tracker.update_person(match_id, features, bbox, center, det["confidence"])

                person = self.tracker.people[match_id]
                gait_features = self.gait_analyzer.extract_features(
                    person.get("trajectory", []),
                    person.get("height_history", []),
                    person.get("speed_history", []),
                )
                person["gait_features"] = gait_features

                label = f"ID {match_id}"
            else:
                person_id = self.tracker.create_person(features, bbox, center, det["confidence"])
                person = self.tracker.people[person_id]
                gait_features = self.gait_analyzer.extract_features(
                    person.get("trajectory", []),
                    person.get("height_history", []),
                    person.get("speed_history", []),
                )
                person["gait_features"] = gait_features

                label = f"ID {person_id}"
                score = 1.0

                if crop is not None and float(det["confidence"]) < 0.70:
                    capture = self.unknown_capture_manager.save_unknown(crop, self.tracker.frame_index)
                    self.unknown_gallery_service.add(capture)
                    label = "Unknown"

            output_detections.append({
                "bbox": self._sanitize_bbox(bbox),
                "label": str(label),
                "match_score": float(score),
                "confidence": float(det["confidence"]),
            })

        self.tracker.mark_inactive()

        annotated = self.annotator.draw(frame, output_detections)
        frame_name = f"frame_{self.tracker.frame_index:06d}.jpg"
        frame_path = OUTPUT_FRAMES_DIR / frame_name
        save_image(frame_path, annotated)

        public_path = f"/static/output_frames/{frame_name}"
        self.stream_service.set_latest_frame(public_path)

        return {
            "frame_index": self.tracker.frame_index,
            "frame_url": public_path,
            "detections": output_detections,
            "active_ids": self.tracker.active_people(),
            "unknown_captures": self.unknown_gallery_service.list_recent(20),
        }