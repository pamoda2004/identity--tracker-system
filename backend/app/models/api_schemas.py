from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str

class StartVideoResponse(BaseModel):
    message: str

class StopVideoResponse(BaseModel):
    message: str