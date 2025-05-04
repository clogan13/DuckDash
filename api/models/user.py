"""
User model for authentication and authorization.
Defines the structure of the 'users' table for login and registration.
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..dependencies.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)  # Unique user ID
    email = Column(String(255), nullable=False, unique=True)     # User's email address (used for login)
    password = Column(String(255), nullable=False)               # Hashed password
    is_active = Column(Boolean, server_default='1', nullable=False)  # Whether the user is active
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  # Account creation timestamp 
    
    # Relationships
    status_changes = relationship("OrderStatusHistory", back_populates="staff_user")
    customer = relationship("Customer", back_populates="user", uselist=False)  # One-to-one relationship with Customer 