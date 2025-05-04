# Customer.py
# Defines the Customer model for the Duckdash application.
# Represents guests/customers in the system.
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, index=True)  # Unique customer ID
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True)  # Link to User model
    first_name = Column(String(100), nullable=False)    # Customer's first name
    last_name = Column(String(100), nullable=False)     # Customer's last name
    phone = Column(String(20))                          # Customer's phone number
    email = Column(String(255))                         # Customer's email address
    address = Column(String(255))                       # Customer's address
    created_at = Column(DateTime)                       # Timestamp when the customer was created
    
    # Relationships
    orders = relationship("Order", back_populates="customer")  # Relationship to orders
    user = relationship("User", back_populates="customer", cascade="all, delete")    # Relationship to user

