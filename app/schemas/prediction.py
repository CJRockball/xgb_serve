from pydantic import BaseModel
from typing import Dict, Any
import uuid
from datetime import datetime

class PredictionBase(BaseModel):
    prediction_type: str
    input_features: Dict[str, Any]
    prediction_result: Dict[str, Any]
    model_version: str
    confidence_score: float
    processing_time_ms: int

class PredictionCreate(PredictionBase):
    pass

class PredictionInDB(PredictionBase):
    id: uuid.UUID
    user_id: uuid.UUID
    request_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Prediction(PredictionInDB):
    pass
