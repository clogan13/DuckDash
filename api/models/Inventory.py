from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
from .ingredient import Ingredient
from .Menu import menu_item_ingredient

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"), nullable=False)
    quantity = Column(DECIMAL(12,2), nullable=False)
    unit_cost = Column(DECIMAL(10,2))
    ingredient = relationship("Ingredient", back_populates="inventory_items")
