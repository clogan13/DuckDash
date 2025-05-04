from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
import enum

class PaymentMethod(str, enum.Enum):
    CARD = "card"
    PAYPAL = "paypal"
    CASH = "cash"
    WALLET = "wallet"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"

class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    transaction_id = Column(String(100))
    payment_time = Column(DateTime)
    order = relationship("Order")
