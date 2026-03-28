import cv2

class FrameAnnotator:
    def draw(self, frame, detections):
        output = frame.copy()

        for det in detections:
            x1, y1, x2, y2 = map(int, det["bbox"])
            label = det["label"]
            score = det["match_score"]

            color = (0, 255, 0) if label != "Unknown" else (0, 0, 255)

            cv2.rectangle(output, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                output,
                f"{label} ({score:.2f})",
                (x1, max(20, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
                cv2.LINE_AA,
            )

        return output