from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import orders as controller
from ..schemas.orders import OrderCreate, OrderUpdate, OrderStatusHistory, Order
from typing import List

# This router handles all order-related API endpoints
router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

# Endpoint to create a new order
@router.post("/", response_model=Order)
def create_order(request: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order.
    If customer_id is not provided, creates a guest customer record.
    """
    return controller.create(db, request)

# Endpoint to get a list of all orders
@router.get("/", response_model=List[Order])
def read_orders(db: Session = Depends(get_db)):
    """
    Get all orders.
    """
    return controller.read_all(db)

# Endpoint to get a single order by its ID
@router.get("/{order_id}", response_model=Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get a specific order by ID.
    """
    return controller.read_one(db, order_id)

# Endpoint to update an order by its ID
@router.put("/{order_id}", response_model=Order)
def update_order(
    order_id: int,
    request: OrderUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an order's status and other details.
    Records status changes in history.
    """
    return controller.update(db, order_id, request)

# Endpoint to delete an order by its ID
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """
    Delete an order.
    """
    return controller.delete(db, order_id)

@router.get("/{order_id}/history", response_model=List[OrderStatusHistory])
def get_order_history(order_id: int, db: Session = Depends(get_db)):
    """
    Get the status history for an order.
    """
    from ..models.Orders import OrderStatusHistory
    history = db.query(OrderStatusHistory).filter(
        OrderStatusHistory.order_id == order_id
    ).order_by(OrderStatusHistory.changed_at.desc()).all()
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No history found for this order"
        )
    return history
