from pydantic import BaseModel

class PersonSignature(BaseModel):
    upper_color: list[float]
    lower_color: list[float]
    aspect_ratio: float
    height: float