from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def detect_people(self, frame):
        results = self.model(frame, verbose=False)
        detections = []

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                cls = int(box.cls.item())
                conf = float(box.conf.item())
                if cls != 0:
                    continue

                x1, y1, x2, y2 = box.xyxy[0].tolist()
                detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": conf,
                    "class_name": "person"
                })

        return detections