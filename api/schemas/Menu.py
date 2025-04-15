from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from .Inventory import InventoryItem

class MenuItem(BaseModel):
    item_name: str

class createMenuItem(BaseModel):
    item_name: str
    price: float
    ingredients: list[str]
    availability: bool

class updateMenuItem(BaseModel):
    item_name: Optional[str] = None
    price: Optional[float] = None
    ingredients: Optional[list[str]] = None
    availability: Optional[bool] = None