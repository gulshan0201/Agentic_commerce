# from fastapi import APIRouter

# router = APIRouter(
#     prefix="/health",
#     tags=["Health"]
# )


# @router.get("")
# def health_check():
#     return {
#         "status": "healthy",
#         "service": "Agentic Commerce Backend"
#     }


# @router.get("/ready")
# def readiness_check():
#     return {
#         "status": "ready"
#     }

from fastapi import APIRouter
from sqlalchemy import text

from app.database import SessionLocal


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
def health_check():
    return {
        "status": "healthy",
        "service": "Agentic Commerce Backend"
    }


@router.get("/ready")
def readiness_check():
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "database": "connected"
        }

    finally:
        db.close()