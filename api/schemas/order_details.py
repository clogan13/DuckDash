from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Schema for creating an order detail (line item)
class OrderDetailCreate(BaseModel):
    menu_item_id: int  # The menu item being ordered
    quantity: int      # How many of this item

# Base schema for order details
class OrderDetailBase(BaseModel):
    amount: int

class OrderDetailCreateOld(OrderDetailBase):
    order_id: int
    menu_id: int

class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_id: Optional[int] = None
    amount: Optional[int] = None

class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    menu_id: int = None

    class Config:
        orm_mode = True