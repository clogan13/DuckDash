from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Base schema for menu item data
class MenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    dietary: Optional[str] = None

# Schema for creating a new menu item
class MenuCreate(MenuBase):
    pass

# Schema for updating a menu item
class MenuUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    dietary: Optional[str] = None

# Schema for returning a menu item from the API
class Menu(MenuBase):
    id: int
    class Config:
        from_attributes = True