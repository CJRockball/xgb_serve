"""
FastAPI application for XGBoost personality prediction model serving.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging

from fastapi.staticfiles import StaticFiles
from app.api.endpoints import health, predict, gui
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.models.model_loader import ModelLoader

# Global model loader instance
model_loader = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown events."""
    global model_loader
    
    # Startup
    settings = get_settings()
    setup_logging(settings.log_level)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting XGBoost Personality Prediction API")
    
    try:
        # Load the model
        model_loader = ModelLoader(settings.xgb_model_path)
        await model_loader.load_model()
        logger.info("Model loaded successfully")
        
        # Store model_loader in app state for access in endpoints
        app.state.model_loader = model_loader
        
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down XGBoost Personality Prediction API")
def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    
    This function encapsulates all app configuration including:
    - FastAPI instance creation with lifecycle management
    - CORS middleware configuration
    - Router inclusion for all endpoints
    - Static file serving for GUI assets
    - Root endpoint definition
    
    Returns:
        FastAPI: The fully configured application instance
    """
    # Create FastAPI app with existing configuration
    app = FastAPI(
        title="XGBoost Personality Prediction API",
        description="API for predicting personality type (Introvert/Extrovert) using XGBoost model",
        version="1.0.0",
        lifespan=lifespan  # Use the existing lifespan function
    )
    
    # Add CORS middleware (preserving your existing configuration)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers (preserving your existing configuration)
    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(predict.router, prefix="/predict", tags=["prediction"])
    app.include_router(gui.router, prefix="/predict", tags=["gui"])  # Add GUI router
    
    # Mount static files for GUI assets
    # This serves CSS/JS files from app/static/ directory
    try:
        app.mount("/static", StaticFiles(directory="app/static"), name="static")
    except RuntimeError:
        # Directory doesn't exist yet - that's fine, GUI will work without custom styling
        logging.getLogger(__name__).info("Static directory not found - GUI will use default styling")
    
    # Root endpoint (preserving your existing functionality)
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "message": "XGBoost Personality Prediction API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/health",
            "gui": "/predict/gui"  # Add GUI reference
        }
    
    return app

# ============================================================================
# REPLACE the original app creation line with this:
# ============================================================================

# Create the application instance using the factory function
app = create_app()


# ============================================================================
# Keep your existing main execution block unchanged:
# ============================================================================

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )