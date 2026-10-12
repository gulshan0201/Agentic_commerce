from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.models.merchant import Merchant
from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db)
):
    merchant = db.get(Merchant, payload.merchant_id)

    if not merchant:
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

    category = db.get(Category, payload.category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    product = Product(**payload.model_dump())

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_products(
    search: str | None = None,
    category_id: int | None = None,
    brand: str | None = None,
    min_price: Decimal | None = Query(default=None, ge=0),
    max_price: Decimal | None = Query(default=None, ge=0),
    in_stock: bool | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

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

    if brand:
        query = query.filter(
            Product.brand.ilike(brand)
        )

    if min_price is not None:
        query = query.filter(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )

    if in_stock is True:
        query = query.filter(
            Product.stock > 0
        )

    if in_stock is False:
        query = query.filter(
            Product.stock == 0
        )

    return query.order_by(Product.id).all()

@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@router.patch(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    updates = payload.model_dump(
        exclude_unset=True
    )

    if "category_id" in updates:
        category = db.get(
            Category,
            updates["category_id"]
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    for field, value in updates.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return None