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
    customer_id: Optional[int] = None  # The ID of the customer placing the order (optional for guests)
    first_name: Optional[str] = None  # Guest first name
    last_name: Optional[str] = None   # Guest last name
    phone: Optional[str] = None       # Guest phone
    email: Optional[str] = None       # Guest email
    address: Optional[str] = None     # Guest address
    tracking_number: str  # Unique tracking number for the order
    status: OrderStatus = OrderStatus.pending  # Order status, defaults to pending
    wait_time_minutes: Optional[int] = None  # Estimated wait time in minutes
    order_details: List[OrderDetailCreate]  # List of items in the order
    promotion_code: Optional[str] = None  # Promotion code (optional)

# Schema for updating an order
class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    status: Optional[OrderStatus] = None
    wait_time_minutes: Optional[int] = None
    notes: Optional[str] = None  # Notes about the status change

# Schema for order status history
class OrderStatusHistory(BaseModel):
    id: int
    order_id: int
    status: OrderStatus
    changed_at: datetime
    changed_by: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

# Schema for returning an order from the API, includes related details
class Order(OrderBase):
    id: int  # Unique order ID
    order_time: Optional[datetime] = None
    items: Optional[List[OrderDetail]] = None
    status_history: Optional[List[OrderStatusHistory]] = None
    customer_id: int
    tracking_number: str
    status: OrderStatus
    total_amount: float
    wait_time_minutes: Optional[int] = None

    class Config:
        from_attributes = True
