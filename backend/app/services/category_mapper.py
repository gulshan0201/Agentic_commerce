from sqlalchemy.orm import Session

from app.models.category import Category


CATEGORY_ALIASES = {
    "laptop": "Laptops",
    "laptops": "Laptops",

    "smartphone": "Smartphones",
    "phone": "Smartphones",
    "mobile": "Smartphones",

    "headphone": "Headphones",
    "headphones": "Headphones",

    "keyboard": "Keyboards",
    "keyboards": "Keyboards",

    "mouse": "Mouse",

    "accessory": "Accessories",
    "accessories": "Accessories"
}


def resolve_category_id(
    db: Session,
    category_name: str | None
) -> int | None:

    if not category_name:
        return None

    normalized = category_name.strip().lower()

    database_name = CATEGORY_ALIASES.get(
        normalized
    )

    if not database_name:
        return None

    category = (
        db.query(Category)
        .filter(
            Category.name == database_name
        )
        .first()
    )

    if not category:
        return None

    return category.id