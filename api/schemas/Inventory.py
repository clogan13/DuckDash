from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InventoryItem(BaseModel):
    resource_name: str
    quantity: int
    price: float

class InventoryCreate(BaseModel):
    pass

class InventoryUpdate(BaseModel):
    resource_name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None

class Inventory(InventoryItem):
    id: int

    class ConfigDict:
        from_attributes = True
