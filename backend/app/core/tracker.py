class SimpleTracker:
    def __init__(self, max_inactive_frames=60, max_history=20):
        self.people = {}
        self.next_id = 1
        self.frame_index = 0
        self.max_inactive_frames = max_inactive_frames
        self.max_history = max_history

    def create_person(self, signature, bbox, center, confidence):
        person_id = self.next_id
        self.next_id += 1

        self.people[person_id] = {
            "person_id": int(person_id),
            "signature": signature,
            "bbox": [float(x) for x in bbox],
            "last_center": (float(center[0]), float(center[1])) if center else None,
            "last_seen_frame": int(self.frame_index),
            "confidence": float(confidence),
            "status": "active",
            "trajectory": [(float(center[0]), float(center[1]))] if center else [],
            "height_history": [float(bbox[3] - bbox[1])],
            "speed_history": [],
            "gait_features": {
                "avg_speed": 0.0,
                "direction_x": 0.0,
                "direction_y": 0.0,
                "vertical_oscillation": 0.0,
                "height_variation": 0.0,
                "movement_confidence": 0.0,
            },
        }
        return person_id

    def update_person(self, person_id, signature, bbox, center, confidence):
        person = self.people[person_id]

        prev_center = person.get("last_center")
        new_center = (float(center[0]), float(center[1])) if center else None

        person["signature"] = signature
        person["bbox"] = [float(x) for x in bbox]
        person["last_center"] = new_center
        person["last_seen_frame"] = int(self.frame_index)
        person["confidence"] = float(confidence)
        person["status"] = "active"

        if new_center:
            person["trajectory"].append(new_center)
            if len(person["trajectory"]) > self.max_history:
                person["trajectory"] = person["trajectory"][-self.max_history:]

        height = float(bbox[3] - bbox[1])
        person["height_history"].append(height)
        if len(person["height_history"]) > self.max_history:
            person["height_history"] = person["height_history"][-self.max_history:]

        if prev_center and new_center:
            dx = new_center[0] - prev_center[0]
            dy = new_center[1] - prev_center[1]
            speed = (dx**2 + dy**2) ** 0.5
            person["speed_history"].append(float(speed))
            if len(person["speed_history"]) > self.max_history:
                person["speed_history"] = person["speed_history"][-self.max_history:]

    def mark_inactive(self):
        for person in self.people.values():
            if self.frame_index - person["last_seen_frame"] > self.max_inactive_frames:
                person["status"] = "inactive"

    def active_people(self):
        return [
            {
                "person_id": int(p["person_id"]),
                "bbox": [float(x) for x in p["bbox"]],
                "confidence": float(p["confidence"]),
                "status": str(p["status"]),
                "last_seen_frame": int(p["last_seen_frame"]),
                "movement_confidence": float(
                    p.get("gait_features", {}).get("movement_confidence", 0.0)
                ),
            }
            for p in self.people.values()
            if p["status"] == "active"
        ]