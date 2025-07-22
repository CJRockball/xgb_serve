"""
Health check endpoints.
"""

import time
import psutil
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any

from app.schemas.response import HealthResponse, MetricsResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# Store startup time for uptime calculation
startup_time = time.time()
prediction_count = 0


@router.get("/", response_model=HealthResponse)
async def health_check(request: Request):
    """
    Basic health check endpoint.
    
    Returns:
        Health status information
    """
    try:
        # Check if model is loaded
        model_loaded = hasattr(request.app.state, 'model_loader') and \
                      request.app.state.model_loader.is_loaded()
        
        return HealthResponse(
            status="healthy" if model_loaded else "unhealthy",
            timestamp=datetime.now(timezone.utc).isoformat(),
            model_loaded=model_loaded
        )
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")


@router.get("/ready", response_model=HealthResponse)
async def readiness_check(request: Request):
    """
    Readiness check endpoint.
    
    Returns:
        Readiness status information
    """
    try:
        # Check if model is loaded and ready
        model_loaded = hasattr(request.app.state, 'model_loader') and \
                      request.app.state.model_loader.is_loaded()
        
        if not model_loaded:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        return HealthResponse(
            status="ready",
            timestamp=datetime.utcnow().isoformat(),
            model_loaded=model_loaded
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Readiness check failed")


@router.get("/live", response_model=HealthResponse)
async def liveness_check(request: Request):
    """
    Liveness check endpoint.
    
    Returns:
        Liveness status information
    """
    try:
        return HealthResponse(
            status="alive",
            timestamp=datetime.utcnow().isoformat(),
            model_loaded=True  # Just check if app is running
        )
    
    except Exception as e:
        logger.error(f"Liveness check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Liveness check failed")


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(request: Request):
    """
    Get application metrics.
    
    Returns:
        Application metrics
    """
    try:
        # Calculate uptime
        uptime_seconds = time.time() - startup_time
        
        # Get memory usage
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_usage_mb = memory_info.rss / 1024 / 1024  # Convert to MB
        
        # Check model status
        model_loaded = hasattr(request.app.state, 'model_loader') and \
                      request.app.state.model_loader.is_loaded()
        
        model_status = "loaded" if model_loaded else "not_loaded"
        
        return MetricsResponse(
            total_predictions=prediction_count,
            model_status=model_status,
            uptime_seconds=uptime_seconds,
            memory_usage_mb=memory_usage_mb
        )
    
    except Exception as e:
        logger.error(f"Metrics collection failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Metrics collection failed")


def increment_prediction_count():
    """Increment the prediction counter."""
    global prediction_count
    prediction_count += 1