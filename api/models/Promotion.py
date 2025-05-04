from sqlalchemy import Column, Integer, String, Date, DECIMAL, Text
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotion"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    discount_amount = Column(DECIMAL(10,2))
    discount_percent = Column(DECIMAL(5,2))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    usage_limit = Column(Integer)
    description = Column(Text)
    menu_items = relationship("Menu", back_populates="promotion")

