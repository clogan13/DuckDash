from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PromotionBase(BaseModel):
    PromotionName: str
    startdate: Optional[datetime]
    enddate: Optional[datetime]
    description: Optional[str]
    deal_percentage: float

class PromotionCreate(PromotionBase):
    PromotionId: int

class PromotionUpdate(PromotionBase):
    PromotionId: Optional[int] = None
    PromotionName: Optional[str] = None
    startdate: Optional[datetime] = None
    enddate: Optional[datetime] = None
    description: Optional[str] = None
    deal_percentage: Optional[float] = None