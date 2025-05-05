from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from api.dependencies.auth import get_current_user
from api.controllers import feedback as controller
from api.schemas.feedback import FeedbackCreate, Feedback
from typing import List
from api.models.user import User

router = APIRouter()

@router.post("/", response_model=Feedback)
def create_feedback(
    request: FeedbackCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Create a new feedback entry.
    If user is logged in, associate it with their account.
    """
    return controller.create(db, request, user.id if user else None)

@router.get("/", response_model=List[Feedback])
def get_feedback(db: Session = Depends(get_db)):
    """
    Get all feedback entries.
    """
    return controller.read_all(db)

@router.get("/{feedback_id}", response_model=Feedback)
def get_feedback_by_id(feedback_id: int, db: Session = Depends(get_db)):
    """
    Get a specific feedback entry by ID.
    """
    feedback = controller.read_one(db, feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    return feedback 