from fastapi import APIRouter
from sqlalchemy import text

from app.database import SessionLocal


router = APIRouter(
    prefix="/database",
    tags=["Database"]
)


@router.get("/test")
def test_database():
    db = SessionLocal()

    try:
        result = db.execute(text("SELECT 1"))
        value = result.scalar()

        return {
            "success": True,
            "message": "Database connection successful",
            "result": value
        }

    finally:
        db.close()