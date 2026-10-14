from fastapi import (
    APIRouter,
    HTTPException
)

from app.schemas.intent import (
    IntentRequest,
    ShoppingIntent
)

from app.services.llm import (
    extract_shopping_intent
)


router = APIRouter(
    prefix="/intent",
    tags=["Intent"]
)


@router.post(
    "/extract",
    response_model=ShoppingIntent
)
def extract_intent(
    payload: IntentRequest
):

    try:

        return extract_shopping_intent(
            payload.message
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Intent extraction failed: {str(exc)}"
        )