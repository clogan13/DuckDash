from pydantic import BaseModel
from typing import Optional

# Base schema for ingredient data
class IngredientBase(BaseModel):
    name: str
    unit: Optional[str] = None

# Schema for creating a new ingredient
class IngredientCreate(IngredientBase):
    pass

# Schema for updating an ingredient
class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None

# Schema for returning an ingredient from the API
class Ingredient(IngredientBase):
    id: int
    class Config:
        orm_mode = True 