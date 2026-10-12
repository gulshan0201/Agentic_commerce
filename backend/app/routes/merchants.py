from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.merchant import Merchant
from app.schemas.merchant import MerchantCreate, MerchantResponse


router = APIRouter(
    prefix="/merchants",
    tags=["Merchants"]
)


@router.post(
    "",
    response_model=MerchantResponse,
    status_code=status.HTTP_201_CREATED
)
def create_merchant(
    payload: MerchantCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(Merchant)
        .filter(Merchant.email == payload.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Merchant email already exists"
        )

    merchant = Merchant(
        name=payload.name,
        email=payload.email
    )

    db.add(merchant)
    db.commit()
    db.refresh(merchant)

    return merchant


@router.get(
    "",
    response_model=list[MerchantResponse]
)
def get_merchants(
    db: Session = Depends(get_db)
):
    return db.query(Merchant).all()