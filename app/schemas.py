"""TO be updated/used Later
from pydantic import BaseModel, Field
from enum import Enum

class Exercise(Enum):
    SQUATS = "squat"
    BICEP_CURL = "bicep_curl"

class ResponseModel(BaseModel):
    rep_count: int
    final_state: str
"""