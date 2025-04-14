from itertools import combinations

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    guest_id = Column("customer.firstname", "customer.lastname")
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    total = Column("total", "payment.payment_amount")
    status = Column(String, nullable=False, server_default="Preparing")

    order_details = relationship("OrderDetail", back_populates="order")