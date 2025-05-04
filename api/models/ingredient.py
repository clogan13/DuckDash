"""
Ingredient model for the database.
Represents an ingredient used in menu items and inventory.
"""
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
from .Menu import menu_item_ingredient

class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)  # Unique ingredient ID
    name = Column(String(100), nullable=False)  # Name of the ingredient
    unit = Column(String(50))  # Unit of measurement (e.g., grams, liters)
    
    # Relationships
    menus = relationship(
        "Menu",
        secondary=menu_item_ingredient,
        back_populates="ingredients"
    )  # Many-to-many relationship with menu items
    inventory_items = relationship("Inventory", back_populates="ingredient")  # Relationship to inventory records 