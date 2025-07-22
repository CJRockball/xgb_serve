# app/api/endpoints/predict.py
"""
Prediction endpoints - OPTIMIZED VERSION
"""

import logging
from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any

from app.schemas.request import SinglePredictionRequest, BatchPredictionRequest
from app.schemas.response import SinglePredictionResponse, BatchPredictionResponse
from app.api.endpoints.health import increment_prediction_count

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/single", response_model=SinglePredictionResponse)
async def predict_single(
    prediction_request: SinglePredictionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start_time = time.time()
    
    try:
        # Make prediction using existing logic
        predictor = request.app.state.predictor
        features = prediction_request.features.dict()
        result = predictor.predict_single(features)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Log prediction to database
        prediction_data = PredictionCreate(
            prediction_type="single",
            input_features=features,
            prediction_result=result,
            model_version=settings.MODEL_VERSION,
            confidence_score=result.get("confidence"),
            processing_time_ms=processing_time
        )
        
        await prediction_crud.create_prediction(
            db, prediction_data, current_user.id
        )
        
        return SinglePredictionResponse(
            success=True,
            result=result,
            message="Prediction completed successfully"
        )
        
    except Exception as e:
        # Log error metrics
        await metrics_service.log_error(db, str(e), current_user.id)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: Request, prediction_request: BatchPredictionRequest):
    """
    Make batch personality predictions using the global predictor instance.
    
    Args:
        request: FastAPI request object  
        prediction_request: Batch prediction request
    
    Returns:
        Batch prediction response
    """
    try:
        # Get the REUSABLE predictor from app state - NO MORE INSTANTIATION!
        if not hasattr(request.app.state, 'predictor'):
            raise HTTPException(status_code=503, detail="Predictor not initialized")
        
        predictor = request.app.state.predictor  # Single line - no object creation!
        
        # Convert features to list of dictionaries
        features_list = [features.to_dict() for features in prediction_request.features]
        
        # Make predictions using the reusable predictor
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