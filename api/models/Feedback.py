from sqlalchemy import Column, Integer, String, DateTime, Text, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    rating = Column(Integer, CheckConstraint('rating BETWEEN 1 AND 5'))
    message = Column(Text)
    created_at = Column(DateTime)
    order = relationship("Order")
    customer = relationship("Customer")

