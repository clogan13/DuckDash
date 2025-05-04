from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Base schema for customer data
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: Optional[str] = None

# Schema for creating a new customer
class CustomerCreate(CustomerBase):
    pass

# Schema for updating a customer
class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

# Schema for returning a customer from the API
class Customer(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 