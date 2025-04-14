from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    payment_method = Column(String)
    payment_status = Column(String)
    payment_date = Column(DATETIME)
    payment_amount = Column(DECIMAL) # combination of menu price, addons, and promotions
