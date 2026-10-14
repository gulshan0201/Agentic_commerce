from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.agent import (
    AgentMessageRequest
)

from app.services.commerce_agent import (
    process_customer_message
)


router = APIRouter(
    prefix="/agent",
    tags=["Commerce Agent"]
)


@router.post("/chat")
def agent_chat(
    payload: AgentMessageRequest,
    db: Session = Depends(get_db)
):

    return process_customer_message(
        db,
        payload.message
    )