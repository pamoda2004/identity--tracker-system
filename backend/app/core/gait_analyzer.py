import math
import numpy as np

class GaitAnalyzer:
    def __init__(self, min_points=5):
        self.min_points = min_points

    def extract_features(self, trajectory, height_history, speed_history):
        """
        Returns simple gait/movement signature.
        """
        if trajectory is None:
            trajectory = []
        if height_history is None:
            height_history = []
        if speed_history is None:
            speed_history = []

        if len(trajectory) < self.min_points:
            return {
                "avg_speed": 0.0,
                "direction_x": 0.0,
                "direction_y": 0.0,
                "vertical_oscillation": 0.0,
                "height_variation": 0.0,
                "movement_confidence": 0.0,
            }

        xs = [p[0] for p in trajectory]
        ys = [p[1] for p in trajectory]

        dxs = [xs[i] - xs[i - 1] for i in range(1, len(xs))]
        dys = [ys[i] - ys[i - 1] for i in range(1, len(ys))]

        speeds = speed_history if len(speed_history) > 0 else [
            math.sqrt(dx * dx + dy * dy) for dx, dy in zip(dxs, dys)
        ]

        avg_speed = float(np.mean(speeds)) if len(speeds) > 0 else 0.0
        direction_x = float(np.mean(dxs)) if len(dxs) > 0 else 0.0
        direction_y = float(np.mean(dys)) if len(dys) > 0 else 0.0

        # walking bounce approximation
        vertical_oscillation = float(np.std(ys)) if len(ys) > 1 else 0.0

        # bbox height changes due to body motion / distance
        height_variation = float(np.std(height_history)) if len(height_history) > 1 else 0.0

        movement_confidence = min(1.0, len(trajectory) / 20.0)

        return {
            "avg_speed": avg_speed,
            "direction_x": direction_x,
            "direction_y": direction_y,
            "vertical_oscillation": vertical_oscillation,
            "height_variation": height_variation,
            "movement_confidence": movement_confidence,
        }

    def compare_features(self, g1, g2):
        """
        Compare two gait signatures and return similarity between 0 and 1.
        """
        if not g1 or not g2:
            return 0.0

        def sim(a, b, scale=1.0):
            diff = abs(a - b)
            value = 1.0 - (diff / max(scale, abs(a), abs(b), 1e-6))
            return max(0.0, min(1.0, value))

        s1 = sim(g1["avg_speed"], g2["avg_speed"], scale=20.0)
        s2 = sim(g1["direction_x"], g2["direction_x"], scale=20.0)
        s3 = sim(g1["direction_y"], g2["direction_y"], scale=20.0)
        s4 = sim(g1["vertical_oscillation"], g2["vertical_oscillation"], scale=20.0)
        s5 = sim(g1["height_variation"], g2["height_variation"], scale=20.0)

        # only trust gait when enough history exists
        confidence_factor = min(g1.get("movement_confidence", 0.0), g2.get("movement_confidence", 0.0))

        raw = (0.25 * s1) + (0.20 * s2) + (0.15 * s3) + (0.25 * s4) + (0.15 * s5)
        return float(raw * confidence_factor + (1 - confidence_factor) * 0.5)