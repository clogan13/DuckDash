from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(String(255))
    created_at = Column(DateTime)
    orders = relationship("Order", back_populates="customer")

