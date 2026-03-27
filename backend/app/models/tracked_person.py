from pydantic import BaseModel

class TrackedPerson(BaseModel):
    person_id: int
    bbox: list[float]
    confidence: float
    status: str
    last_seen_frame: int
    trajectory: list[tuple[float, float]] = []
    height_history: list[float] = []
    speed_history: list[float] = []
    gait_features: dict = {}