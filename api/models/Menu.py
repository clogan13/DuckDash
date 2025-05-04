from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Text, Enum, Table
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

menu_item_ingredient = Table(
    "menu_item_ingredient",
    Base.metadata,
    Column("menu_item_id", Integer, ForeignKey("menu_item.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"), primary_key=True),
    Column("quantity", Integer),  # or DECIMAL if you want
)

class Menu(Base):
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10,2), nullable=False)
    category = Column(String(50))
    dietary = Column(String(50))
    promotion_id = Column(Integer, ForeignKey("promotion.id"))
    promotion = relationship("Promotion", back_populates="menu_items")
    ingredients = relationship(
        "Ingredient",
        secondary=menu_item_ingredient,
        back_populates="menus"
    )




