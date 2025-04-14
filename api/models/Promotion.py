from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class promotion(Base):
    __tablename__ = 'promotion'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    discount = Column(DECIMAL)
    start_date = Column(DATETIME)
    end_date = Column(DATETIME)

