from ctypes.wintypes import BOOLEAN

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    item = Column(String)
    ingredients = Column("inventory.item_name", String)
    standard_price = Column(DECIMAL)
    availability = Column(BOOLEAN)
    rating = Column(DECIMAL)
    description = Column(String)




