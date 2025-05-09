from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
import enum
from datetime import datetime

class OrderStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    preparing = "preparing"
    ready = "ready"
    completed = "completed"
    delivered = "delivered"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    tracking_number = Column(String(100), unique=True, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.pending)
    total_amount = Column(DECIMAL(10,2), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    promotion_code = Column(String(50))
    discount_amount = Column(DECIMAL(10,2), default=0)
    wait_time_minutes = Column(Integer)
    
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    status_history = relationship("OrderStatusHistory", back_populates="order")
    payments = relationship("Payment", back_populates="order")

class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    changed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text)
    order = relationship("Order", back_populates="status_history")
    staff_user = relationship("User", back_populates="status_changes")

class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_item.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    item_price = Column(DECIMAL(10,2), nullable=False)
    order = relationship("Order", back_populates="items")
    menu_item = relationship("Menu")
