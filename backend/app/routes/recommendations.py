from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse
)

from app.services.recommendation import (
    recommend_products
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.post(
    "",
    response_model=RecommendationResponse
)
def get_recommendations(
    payload: RecommendationRequest,
    db: Session = Depends(get_db)
):

    category = db.get(
        Category,
        payload.category_id
    )

    if not category:

        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    recommendations = (
        recommend_products(
            db,
            payload
        )
    )

    return {
        "total_matches": len(
            recommendations
        ),
        "recommendations": (
            recommendations[:5]
        )
    }