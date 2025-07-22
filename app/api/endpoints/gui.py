from fastapi import APIRouter, Request, Form, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.predictor import PersonalityPredictor  # Import PersonalityPredictor directly
import logging

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)

# ------------------------------#
# Render empty GUI form (GET)    #
# ------------------------------#
@router.get(
    "/gui",
    response_class=HTMLResponse,
    tags=["GUI"],
    summary="Render GUI form for single prediction",
)
async def render_gui(request: Request):
    """Render the GUI form for single prediction"""
    return templates.TemplateResponse(
        name="gui_form.html",
        context={"request": request, "result": None}
    )

# -----------------------------------#
# Handle submitted form data (POST)   #
# -----------------------------------#
@router.post(
    "/gui",
    response_class=HTMLResponse,
    tags=["GUI"],
    summary="Handle form submission and show prediction",
)
async def handle_gui(
    request: Request,
    time_spent_alone: float = Form(...),
    stage_fear: str = Form(...),
    social_event_attendance: float = Form(...),
    going_outside: float = Form(...),
    drained_after_socializing: str = Form(...),
    friends_circle_size: float = Form(...),
    post_frequency: float = Form(...),
):
    """Handle form submission and show prediction result"""
    try:
        # Build feature dict identical to API schema
        features = {
            "time_spent_alone": time_spent_alone,
            "stage_fear": stage_fear,
            "social_event_attendance": social_event_attendance,
            "going_outside": going_outside,
            "drained_after_socializing": drained_after_socializing,
            "friends_circle_size": friends_circle_size,
            "post_frequency": post_frequency,
        }

        # Get model loader from app state (same approach as predict.py)
        if not hasattr(request.app.state, 'model_loader'):
            raise HTTPException(status_code=503, detail="Model not initialized")
        
        model_loader = request.app.state.model_loader
        
        if not model_loader.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Create predictor instance (same as predict.py)
        predictor = PersonalityPredictor(model_loader)
        
        # Make prediction directly using PersonalityPredictor
        prediction_result = predictor.predict_single(features)
        
        logger.info(f"GUI prediction successful: {prediction_result}")

        # Render result page
        return templates.TemplateResponse(
            name="gui_result.html",
            context={
                "request": request,
                "result": prediction_result,  # This contains the actual prediction data
                "input": features,
            },
            status_code=status.HTTP_200_OK,
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"GUI prediction failed: {str(e)}")
        
        # Render error in the form
        return templates.TemplateResponse(
            name="gui_form.html",
            context={
                "request": request,
                "result": None,
                "error_message": f"Prediction failed: {str(e)}"
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
