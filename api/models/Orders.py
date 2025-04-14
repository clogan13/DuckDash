from itertools import combinations

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    guest_id = Column(Integer, ForeignKey("guests.id"))
    guest_name= Column("customer.first_name" + "customer.last_name")
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    total = Column( "payment.payment_amount")
    status = Column(String, nullable=False, server_default="Preparing")
