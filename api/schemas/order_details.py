from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Schema for creating an order detail (line item)
class OrderDetailCreate(BaseModel):
    menu_item_id: int  # The menu item being ordered
    quantity: int      # How many of this item
    # item_price removed; backend will calculate

# Base schema for order details
class OrderDetailBase(BaseModel):
    quantity: int
    item_price: float

class OrderDetailCreateOld(OrderDetailBase):
    order_id: int
    menu_item_id: int

class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    quantity: Optional[int] = None
    item_price: Optional[float] = None

class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    menu_item_id: int

    class Config:
        from_attributes = True