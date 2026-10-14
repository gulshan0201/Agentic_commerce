from sqlalchemy.orm import Session

from app.schemas.recommendation import RecommendationRequest
from app.services.category_mapper import resolve_category_id

from app.services.category_mapper import (
    resolve_category_id
)

from app.services.llm import (
    extract_shopping_intent
)

from app.services.recommendation import (
    recommend_products
)


def process_customer_message(
    db: Session,
    message: str
):

    intent = extract_shopping_intent(
        message
    )

    category_id = resolve_category_id(
        db,
        intent.category
    )

    if category_id is None:

        return {
            "status": "needs_information",
            "message": (
                "I couldn't determine which product "
                "category you are looking for."
            ),
            "missing_fields": [
                "category"
            ],
            "intent": intent.model_dump()
        }

    if intent.budget_max is None:

        return {
            "status": "needs_information",
            "message": (
                "What is the maximum budget "
                "you would like to spend?"
            ),
            "missing_fields": [
                "budget_max"
            ],
            "intent": intent.model_dump()
        }

    request = RecommendationRequest(
        category_id=category_id,
        budget_max=intent.budget_max,
        use_case=intent.use_case,
        minimum_ram=intent.minimum_ram,
        gpu_required=intent.gpu_required,
        minimum_rating=intent.minimum_rating,
        in_stock_only=intent.in_stock_only
    )

    recommendations = recommend_products(
        db,
        request
    )

    if not recommendations:

        return {
            "status": "no_matches",
            "message": (
                "I couldn't find a product matching "
                "all of those requirements."
            ),
            "intent": intent.model_dump(),
            "recommendations": []
        }

    best = recommendations[0]

    return {
        "status": "success",
        "message": (
            f"My top recommendation is "
            f"{best['name']} at ₹{best['price']}."
        ),
        "intent": intent.model_dump(),
        "recommendations": recommendations[:5]
    }