import math
from app.utils.color_utils import color_similarity
from app.core.gait_analyzer import GaitAnalyzer


class IdentityMatcher:
    def __init__(self, threshold: float = 0.70):
        self.threshold = threshold
        self.gait_analyzer = GaitAnalyzer()

    def _ratio_similarity(self, r1, r2):
        if r1 <= 0 or r2 <= 0:
            return 0.0
        diff = abs(r1 - r2)
        base = max(r1, r2)
        sim = 1.0 - (diff / base)
        return max(0.0, min(1.0, sim))

    def _position_similarity(self, c1, c2, frame_diag=1500.0):
        if c1 is None or c2 is None:
            return 0.0
        dx = c1[0] - c2[0]
        dy = c1[1] - c2[1]
        dist = math.sqrt(dx * dx + dy * dy)
        sim = 1.0 - (dist / frame_diag)
        return max(0.0, min(1.0, sim))

    def compare(self, a, b, center_a=None, center_b=None, gait_a=None, gait_b=None):
        upper = color_similarity(a["upper_color"], b["upper_color"])
        lower = color_similarity(a["lower_color"], b["lower_color"])
        ratio = self._ratio_similarity(a["aspect_ratio"], b["aspect_ratio"])
        pos = self._position_similarity(center_a, center_b)

        gait_score = 0.0
        if gait_a is not None and gait_b is not None:
            gait_score = self.gait_analyzer.compare_features(gait_a, gait_b)

        score = (
            0.30 * upper +
            0.25 * lower +
            0.15 * ratio +
            0.10 * pos +
            0.20 * gait_score
        )
        return round(score, 4)

    def best_match(self, current_features, current_center, tracked_people, current_gait=None):
        best_id = None
        best_score = 0.0

        for person_id, person in tracked_people.items():
            score = self.compare(
                current_features,
                person["signature"],
                current_center,
                person.get("last_center"),
                current_gait,
                person.get("gait_features"),
            )
            if score > best_score:
                best_score = score
                best_id = person_id

        if best_score >= self.threshold:
            return best_id, best_score

        return None, best_score