"""
Prediction endpoints.
"""

import logging
from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any

from app.schemas.request import SinglePredictionRequest, BatchPredictionRequest
from app.schemas.response import SinglePredictionResponse, BatchPredictionResponse, ErrorResponse
from app.models.predictor import PersonalityPredictor
from app.api.endpoints.health import increment_prediction_count

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/single", response_model=SinglePredictionResponse)
async def predict_single(request: Request, prediction_request: SinglePredictionRequest):
    """
    Make a single personality prediction.
    
    Args:
        request: FastAPI request object
        prediction_request: Single prediction request
        
    Returns:
        Single prediction response
    """
    try:
        # Get model loader from app state
        if not hasattr(request.app.state, 'model_loader'):
            raise HTTPException(status_code=503, detail="Model not initialized")
        
        model_loader = request.app.state.model_loader
        
        if not model_loader.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Create predictor
        predictor = PersonalityPredictor(model_loader)
        
        # Convert features to dictionary
        features = prediction_request.features.to_dict()
        
        # Make prediction
        result = predictor.predict_single(features)
        
        # Increment prediction counter
        increment_prediction_count()
        
        return SinglePredictionResponse(
            success=True,
            result=result,
            message="Prediction completed successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Single prediction failed: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: Request, prediction_request: BatchPredictionRequest):
    """
    Make batch personality predictions.
    
    Args:
        request: FastAPI request object
        prediction_request: Batch prediction request
        
    Returns:
        Batch prediction response
    """
    try:
        # Get model loader from app state
        if not hasattr(request.app.state, 'model_loader'):
            raise HTTPException(status_code=503, detail="Model not initialized")
        
        model_loader = request.app.state.model_loader
        
        if not model_loader.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Create predictor
        predictor = PersonalityPredictor(model_loader)
        
        # Convert features to list of dictionaries
        features_list = [features.to_dict() for features in prediction_request.features]
        
        # Make predictions
        results = predictor.predict_batch(features_list)
        
        # Increment prediction counter
        for _ in results:
            increment_prediction_count()
        
        return BatchPredictionResponse(
            success=True,
            results=results,
            count=len(results),
            message="Batch prediction completed successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch prediction failed: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Batch prediction failed: {str(e)}"
        )


@router.get("/example")
async def get_example():
    """
    Get example request format.
    
    Returns:
        Example request format
    """
    return {
        "single_prediction_example": {
            "features": {
                "time_spent_alone": 5.0,
                "stage_fear": "No",
                "social_event_attendance": 7.0,
                "going_outside": 6.0,
                "drained_after_socializing": "Yes",
                "friends_circle_size": 8.0,
                "post_frequency": 4.0
            }
        },
        "batch_prediction_example": {
            "features": [
                {
                    "time_spent_alone": 5.0,
                    "stage_fear": "No",
                    "social_event_attendance": 7.0,
                    "going_outside": 6.0,
                    "drained_after_socializing": "Yes",
                    "friends_circle_size": 8.0,
                    "post_frequency": 4.0
                },
                {
                    "time_spent_alone": 2.0,
                    "stage_fear": "Yes",
                    "social_event_attendance": 3.0,
                    "going_outside": 2.0,
                    "drained_after_socializing": "No",
                    "friends_circle_size": 12.0,
                    "post_frequency": 8.0
                }
            ]
        }
    }