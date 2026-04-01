from app.config import VIDEO_SOURCE, OUTPUT_FRAMES_DIR, MATCH_THRESHOLD, UNKNOWN_DIR
from app.core.detector import PersonDetector
from app.core.feature_extractor import FeatureExtractor
from app.core.identity_matcher import IdentityMatcher
from app.core.tracker import SimpleTracker
from app.core.unknown_capture import UnknownCaptureManager
from app.core.annotator import FrameAnnotator
from app.core.gait_analyzer import GaitAnalyzer
from app.utils.image_utils import crop_bbox, center_of_bbox, save_image

import cv2


class TrackingService:
    def __init__(
        self,
        model_path,
        max_inactive_frames,
        unknown_gallery_service,
        stream_service,
        named_registry_service,
    ):
        self.detector = PersonDetector(model_path)
        self.extractor = FeatureExtractor()
        self.matcher = IdentityMatcher(MATCH_THRESHOLD)
        self.gait_analyzer = GaitAnalyzer()
        self.tracker = SimpleTracker(max_inactive_frames=max_inactive_frames)
        self.unknown_capture_manager = UnknownCaptureManager(unknown_dir=UNKNOWN_DIR)
        self.annotator = FrameAnnotator()
        self.unknown_gallery_service = unknown_gallery_service
        self.stream_service = stream_service
        self.named_registry_service = named_registry_service
        self.cap = None
        self.running = False
        self.video_source = VIDEO_SOURCE

    def _sanitize_bbox(self, bbox):
        return [float(x) for x in bbox]

    def _is_valid_for_new_id(self, det, bbox, crop):
        if crop is None:
            return False

        conf = float(det["confidence"])
        x1, y1, x2, y2 = bbox
        w = float(x2 - x1)
        h = float(y2 - y1)

        # valid enough detection for creating a current active ID
        if conf < 0.45:
            return False
        if w < 30 or h < 60:
            return False

        return True

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

            current_gait = {
                "avg_speed": 0.0,
                "direction_x": 0.0,
                "direction_y": 0.0,
                "vertical_oscillation": 0.0,
                "height_variation": 0.0,
                "movement_confidence": 0.0,
            }

            # 1) Try current active tracked IDs
            match_id, score = self.matcher.best_match(
                features,
                center,
                self.tracker.people,
                current_gait=current_gait
            )

            if match_id is not None and score >= MATCH_THRESHOLD:
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
                # 2) Try named registry
                named_match, named_score = self.named_registry_service.find_best_match(
                    features,
                    self.matcher
                )

                if named_match is not None and named_score >= MATCH_THRESHOLD:
                    label = named_match["name"]
                    score = named_score

                else:
                    # 3) If no active ID and no named match:
                    # create CURRENT ACTIVE ID if valid, otherwise Unknown list
                    if self._is_valid_for_new_id(det, bbox, crop):
                        person_id = self.tracker.create_person(
                            features, bbox, center, det["confidence"]
                        )

                        person = self.tracker.people[person_id]
                        gait_features = self.gait_analyzer.extract_features(
                            person.get("trajectory", []),
                            person.get("height_history", []),
                            person.get("speed_history", []),
                        )
                        person["gait_features"] = gait_features

                        label = f"ID {person_id}"
                        score = 1.0
                    else:
                        label = "Unknown"
                        score = max(score, named_score if 'named_score' in locals() else 0.0)

                        if crop is not None:
                            capture = self.unknown_capture_manager.save_unknown(
                                crop,
                                self.tracker.frame_index,
                                signature=features
                            )
                            self.unknown_gallery_service.add(capture)

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
            "frame_index": int(self.tracker.frame_index),
            "frame_url": public_path,
            "detections": output_detections,
            "active_ids": self.tracker.active_people(),
            "unknown_captures": self.unknown_gallery_service.list_recent(20),
            "named_people": self.named_registry_service.list_all(),
        }