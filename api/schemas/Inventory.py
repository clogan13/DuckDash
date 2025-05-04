from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Base schema for inventory data
class InventoryBase(BaseModel):
    ingredient_id: int
    quantity: float
    unit_cost: Optional[float] = None

# Schema for creating a new inventory item
class InventoryCreate(InventoryBase):
    pass

# Schema for updating an inventory item
class InventoryUpdate(BaseModel):
    ingredient_id: Optional[int] = None
    quantity: Optional[float] = None
    unit_cost: Optional[float] = None

# Schema for returning an inventory item from the API
class Inventory(InventoryBase):
    id: int
    class Config:
        orm_mode = True
