from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class FeedBackBase(BaseModel):
    rating: float
    description: str


class FeedbackCreate(FeedBackBase):
    feedback_id: int
    rating: float
    description: Optional[str] = None

class FeedbackUpdate(FeedBackBase):
    feedback_id: int
    rating: Optional[float] = None
    description: Optional[str] = None

class Feedback(FeedBackBase):
    feedback_id: int

    class Config:
        from_attributes = True