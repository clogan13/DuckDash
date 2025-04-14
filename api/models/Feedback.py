from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey('customer.id'))
    order_id = Column(Integer, ForeignKey('order.id'))
    rating = Column(DECIMAL)
    comment = Column(String)

