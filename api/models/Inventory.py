from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
from .Menu import menu_item_ingredient

class Ingredient(Base):
    __tablename__ = "ingredient"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(50))
    menus = relationship(
        "Menu",
        secondary=menu_item_ingredient,
        back_populates="ingredients"
    )
    inventory_items = relationship("Inventory", back_populates="ingredient")

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"), nullable=False)
    quantity = Column(DECIMAL(12,2), nullable=False)
    unit_cost = Column(DECIMAL(10,2))
    ingredient = relationship("Ingredient", back_populates="inventory_items")
