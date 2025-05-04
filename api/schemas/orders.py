from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail, OrderDetailCreate

# Base schema for order data
class OrderBase(BaseModel):
    description: Optional[str] = None  # Optional order description

# Schema for creating a new order, including order details
class OrderCreate(OrderBase):
    customer_id: int  # The ID of the customer placing the order
    order_details: List[OrderDetailCreate]  # List of items in the order

# Schema for updating an order
class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    description: Optional[str] = None

# Schema for returning an order from the API, includes related details
class Order(OrderBase):
    id: int  # Unique order ID
    order_date: Optional[datetime] = None
    order_details: Optional[List[OrderDetail]] = None
    customer_id: int

    class Config:
        orm_mode = True  # Enables compatibility with ORM objects
