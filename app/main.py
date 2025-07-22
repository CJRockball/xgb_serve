# app/main.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.models.model_loader import ModelLoader
from app.models.predictor import PersonalityPredictor  # Import predictor
from app.api.endpoints import predict, health, gui

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown events."""
    # Startup
    logger.info("Starting up XGBoost Personality Prediction API...")
    
    settings = get_settings()
    
    # Initialize model loader
    model_loader = ModelLoader(settings.xgb_model_path)
    await model_loader.load_model()
    
    # Initialize single predictor instance - THIS IS THE KEY CHANGE
    predictor = PersonalityPredictor(model_loader)
    
    # Store both in app state
    app.state.model_loader = model_loader
    app.state.predictor = predictor  # Store the single predictor instance
    
    logger.info("Model and predictor initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")

def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title="XGBoost Personality Prediction API",
        description="API for personality prediction using XGBoost model",
        version="1.0.0",
        lifespan=lifespan  # Use the lifespan context manager
    )
    
    # Include routers
    app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
    app.include_router(health.router, tags=["Health"])
    app.include_router(gui.router, prefix="/predict", tags=["GUI"])
    
    # Mount static files
    try:
        app.mount("/static", StaticFiles(directory="app/static"), name="static")
    except RuntimeError:
        logger.info("Static directory not found - GUI will use default styling")
    
    return app

app = create_app()
