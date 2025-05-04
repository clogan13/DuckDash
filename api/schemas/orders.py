from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail, OrderDetailCreate
from ..models.Orders import OrderStatus

# Base schema for order data
class OrderBase(BaseModel):
    pass

# Schema for creating a new order, including order details
class OrderCreate(OrderBase):
    customer_id: int  # The ID of the customer placing the order
    tracking_number: str  # Unique tracking number for the order
    status: OrderStatus = OrderStatus.pending  # Order status, defaults to pending
    wait_time_minutes: Optional[int] = None  # Estimated wait time in minutes
    order_details: List[OrderDetailCreate]  # List of items in the order

# Schema for updating an order
class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    status: Optional[OrderStatus] = None
    wait_time_minutes: Optional[int] = None

# Schema for returning an order from the API, includes related details
class Order(OrderBase):
    id: int  # Unique order ID
    order_time: Optional[datetime] = None
    items: Optional[List[OrderDetail]] = None
    customer_id: int
    tracking_number: str
    status: OrderStatus
    total_amount: float
    wait_time_minutes: Optional[int] = None

    class Config:
        from_attributes = True  # Enables compatibility with ORM objects
