# app/api/endpoints/gui.py - OPTIMIZED VERSION
from fastapi import APIRouter, Request, Form, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import logging

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)

@router.get("/gui", response_class=HTMLResponse, tags=["GUI"])
async def render_gui(request: Request):
    """Render the GUI form for single prediction"""
    return templates.TemplateResponse(
        "gui_form.html",
        {"request": request, "result": None}
    )

@router.post("/gui", response_class=HTMLResponse, tags=["GUI"])
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
    """Handle form submission using the global predictor instance."""
    try:
        # Build feature dict
        features = {
            "time_spent_alone": time_spent_alone,
            "stage_fear": stage_fear,
            "social_event_attendance": social_event_attendance,
            "going_outside": going_outside,
            "drained_after_socializing": drained_after_socializing,
            "friends_circle_size": friends_circle_size,
            "post_frequency": post_frequency,
        }

        # Get the REUSABLE predictor from app state - NO MORE INSTANTIATION!
        if not hasattr(request.app.state, 'predictor'):
            raise HTTPException(status_code=503, detail="Predictor not initialized")
        
        predictor = request.app.state.predictor  # Single line - no object creation!
        
        # Make prediction using the reusable predictor
        prediction_result = predictor.predict_single(features)
        
        logger.info(f"GUI prediction successful: {prediction_result}")

        # Render result page
        return templates.TemplateResponse(
            name="gui_result.html",
            context={
                "request": request,
                "result": prediction_result,
                "input": features,
            },
            status_code=status.HTTP_200_OK,
        )
        
    except HTTPException:
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
