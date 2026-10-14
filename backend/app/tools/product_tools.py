from decimal import Decimal

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.product import Product


def search_products(
    db: Session,
    search: str | None = None,
    category_id: int | None = None,
    max_price: Decimal | None = None,
    min_price: Decimal | None = None,
    in_stock_only: bool = True,
    limit: int = 10
):

    query = db.query(Product).filter(
        Product.is_active.is_(True)
    )

    if search:

        pattern = f"%{search}%"

        query = query.filter(
            or_(
                Product.name.ilike(pattern),
                Product.brand.ilike(pattern),
                Product.description.ilike(pattern)
            )
        )

    if category_id is not None:

        query = query.filter(
            Product.category_id == category_id
        )

    if min_price is not None:

        query = query.filter(
            Product.price >= min_price
        )

    if max_price is not None:

        query = query.filter(
            Product.price <= max_price
        )

    if in_stock_only:

        query = query.filter(
            Product.stock > 0
        )

    return (
        query
        .order_by(Product.rating.desc())
        .limit(limit)
        .all()
    )


def get_product(
    db: Session,
    product_id: int
):

    return db.get(
        Product,
        product_id
    )


def check_stock(
    db: Session,
    product_id: int
):

    product = db.get(
        Product,
        product_id
    )

    if not product:

        return None

    return {
        "product_id": product.id,
        "name": product.name,
        "stock": product.stock,
        "available": product.stock > 0
    }


def compare_products(
    db: Session,
    product_ids: list[int]
):

    products = (
        db.query(Product)
        .filter(
            Product.id.in_(product_ids)
        )
        .all()
    )

    return products