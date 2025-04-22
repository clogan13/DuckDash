from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaymentBase(BaseModel):
    amount: float
    currency: str

class PaymentCreate(BaseModel):
    amount: float
    currency: str

class PaymentUpdate(BaseModel):
    amount: float
    currency: str

class Payment(PaymentBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True
