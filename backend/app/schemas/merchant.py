from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class MerchantBase(BaseModel):
    name: str
    email: EmailStr


class MerchantCreate(MerchantBase):
    pass


class MerchantResponse(MerchantBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)