from pydantic import BaseModel

class DetectionResult(BaseModel):
    bbox: list[float]
    confidence: float
    class_name: str