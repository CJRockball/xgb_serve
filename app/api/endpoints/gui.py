from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.api.endpoints.predict import predict_single  # Re-use existing logic

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ------------------------------ #
# Render empty GUI form (GET)    #
# ------------------------------ #
@router.get(
    "/gui",
    response_class=HTMLResponse,
    tags=["GUI"],
    summary="Render GUI form for single prediction",
)
async def render_gui(request: Request):
    return templates.TemplateResponse(
        name="gui_form.html",
        context={"request": request, "result": None}
    )

# ----------------------------------- #
# Handle submitted form data (POST)   #
# ----------------------------------- #
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

    # Call existing service function
    prediction = await predict_single(features)

    # Render result page
    return templates.TemplateResponse(
        name="gui_result.html",
        context={
            "request": request,
            "result": prediction,
            "input": features,
        },
        status_code=status.HTTP_200_OK,
    )
