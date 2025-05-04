"""
Schemas for ingredient-related operations.
"""
from pydantic import BaseModel
from typing import Optional

class IngredientBase(BaseModel):
    """
    Base schema for ingredient data.
    """
    name: str
    unit: Optional[str] = None

class IngredientCreate(IngredientBase):
    """
    Schema for creating a new ingredient.
    """
    pass

class IngredientUpdate(BaseModel):
    """
    Schema for updating an existing ingredient.
    """
    name: Optional[str] = None
    unit: Optional[str] = None

class Ingredient(IngredientBase):
    """
    Schema for ingredient response.
    """
    id: int

    class Config:
        from_attributes = True 