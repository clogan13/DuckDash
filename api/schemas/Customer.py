from pydantic import BaseModel
from typing import Optional

# Base schema for customer data. Used for both creation and response.
class CustomerBase(BaseModel):
    first_name: str  # Customer's first name
    last_name: str   # Customer's last name
    email: Optional[str] = None  # Optional email address
    phone: Optional[str] = None  # Optional phone number
    address: Optional[str] = None  # Optional address

# Schema for creating a new customer (inherits all fields from CustomerBase)
class CustomerCreate(CustomerBase):
    pass

# Schema for returning a customer from the API, includes the database ID
class Customer(CustomerBase):
    id: int  # Unique customer ID from the database
    class Config:
        orm_mode = True  # Enables compatibility with ORM objects 