# Menu.py
# Defines the Menu model and the association table for menu items and ingredients.
from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Text, Enum, Table
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

# Association table for many-to-many relationship between menu items and ingredients
menu_item_ingredient = Table(
    "menu_item_ingredient",
    Base.metadata,
    Column("menu_item_id", Integer, ForeignKey("menu_item.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"), primary_key=True),
    Column("quantity", Integer),  # Quantity of ingredient in the menu item
)

class Menu(Base):
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key=True, index=True)  # Unique menu item ID
    name = Column(String(150), nullable=False)          # Name of the menu item
    description = Column(Text)                          # Description of the menu item
    price = Column(DECIMAL(10,2), nullable=False)       # Price of the menu item
    category = Column(String(50))                       # Category (e.g., appetizer, main course)
    dietary = Column(String(50))                        # Dietary info (e.g., vegan, gluten-free)
    promotion_id = Column(Integer, ForeignKey("promotion.id"))  # Associated promotion (if any)
    promotion = relationship("Promotion", back_populates="menu_items")  # Relationship to promotion
    ingredients = relationship(
        "Ingredient",
        secondary=menu_item_ingredient,
        back_populates="menus"
    )  # Many-to-many relationship with ingredients




