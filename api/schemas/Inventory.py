from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InventoryItem(BaseModel):
    resource_name: str
    quantity: int
    quantity: int
    price: float

