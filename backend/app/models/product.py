from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    Numeric,
    String
)

from sqlalchemy.sql import func

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    merchant_id = Column(
        Integer,
        ForeignKey("merchants.id"),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    name = Column(
        String(200),
        nullable=False
    )

    brand = Column(
        String(100),
        nullable=True
    )

    description = Column(
        String(1000),
        nullable=True
    )

    price = Column(
    Numeric(12, 2),
    nullable=False
    )

    stock = Column(
        Integer,
        default=0
    )

    rating = Column(
        Float,
        nullable=True
    )

    specifications = Column(
        JSON,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )