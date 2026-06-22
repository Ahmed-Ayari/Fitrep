from pydantic import BaseModel, Field
from enum import Enum

class Exercice(Enum):
    SQUATS = "squat"
    BICEP_CURL = "bicep_curl"

class ResponseModel(BaseModel):
    rep_count: int
    final_state: str