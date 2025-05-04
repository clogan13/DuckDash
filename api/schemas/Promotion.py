from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PromotionBase(BaseModel):
    code: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    discount_percent: Optional[float] = None
    discount_amount: Optional[float] = None

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(PromotionBase):
    pass

class PromotionResponse(PromotionBase):
    id: int
    class Config:
        from_attributes = True