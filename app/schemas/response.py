"""
Response schemas for the API.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class PredictionResult(BaseModel):
    """Single prediction result."""
    
    prediction: str = Field(
        ..., 
        description="Predicted personality type (Introvert/Extrovert)"
    )
    prediction_code: int = Field(
        ..., 
        description="Prediction code (0=Introvert, 1=Extrovert)"
    )
    probabilities: Dict[str, float] = Field(
        ..., 
        description="Prediction probabilities for each class"
    )
    confidence: float = Field(
        ..., 
        description="Confidence of the prediction (max probability)"
    )


class SinglePredictionResponse(BaseModel):
    """Response for single prediction."""
    
    success: bool = Field(True, description="Whether the prediction was successful")
    result: PredictionResult = Field(..., description="Prediction result")
    message: str = Field("Prediction completed successfully", description="Response message")


class BatchPredictionResponse(BaseModel):
    """Response for batch prediction."""
    
    success: bool = Field(True, description="Whether the prediction was successful")
    results: List[PredictionResult] = Field(..., description="List of prediction results")
    count: int = Field(..., description="Number of predictions made")
    message: str = Field("Batch prediction completed successfully", description="Response message")


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field("healthy", description="Health status")
    timestamp: str = Field(..., description="Response timestamp")
    version: str = Field("1.0.0", description="API version")
    model_loaded: bool = Field(..., description="Whether the model is loaded")


class MetricsResponse(BaseModel):
    """Metrics response."""
    
    total_predictions: int = Field(..., description="Total number of predictions made")
    model_status: str = Field(..., description="Model status")
    uptime_seconds: float = Field(..., description="Application uptime in seconds")
    memory_usage_mb: float = Field(..., description="Memory usage in MB")


class ErrorResponse(BaseModel):
    """Error response."""
    
    success: bool = Field(False, description="Whether the operation was successful")
    error: str = Field(..., description="Error message")
    details: str = Field(None, description="Additional error details")