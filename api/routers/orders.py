from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.orders import OrderCreate, OrderUpdate, Order
from ..controllers import orders as controller
from typing import List

# This router handles all order-related API endpoints
router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

# Endpoint to create a new order
@router.post("/", response_model=Order)
def create_order(request: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order and return the created order with its ID."""
    return controller.create(db=db, request=request)

# Endpoint to get a list of all orders
@router.get("/", response_model=List[Order])
def get_orders(db: Session = Depends(get_db)):
    """Retrieve all orders from the database."""
    return controller.read_all(db)

# Endpoint to get a single order by its ID
@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Retrieve an order by its unique ID."""
    return controller.read_one(db, order_id)

# Endpoint to update an order by its ID
@router.put("/{order_id}", response_model=Order)
def update_order(order_id: int, request: OrderUpdate, db: Session = Depends(get_db)):
    """Update an order's details by its ID."""
    return controller.update(db, order_id, request)

# Endpoint to delete an order by its ID
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order by its unique ID."""
    return controller.delete(db, order_id)
