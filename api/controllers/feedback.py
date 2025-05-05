from sqlalchemy.orm import Session
from api.models.feedback import Feedback
from api.schemas.feedback import FeedbackCreate
from typing import List

def create(db: Session, feedback: FeedbackCreate, user_id: int = None) -> Feedback:
    """
    Create a new feedback entry.
    """
    db_feedback = Feedback(
        name=feedback.name,
        email=feedback.email,
        subject=feedback.subject,
        message=feedback.message,
        user_id=user_id
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def read_all(db: Session) -> List[Feedback]:
    """
    Get all feedback entries.
    """
    return db.query(Feedback).all()

def read_one(db: Session, feedback_id: int) -> Feedback:
    """
    Get a specific feedback entry by ID.
    """
    return db.query(Feedback).filter(Feedback.id == feedback_id).first() 