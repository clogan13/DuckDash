from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from api.dependencies.auth import get_current_user
from api.controllers import orders as controller
from api.schemas.orders import OrderCreate, OrderUpdate, OrderStatusHistory, Order
from typing import List
from api.models.user import User
from api.models.Customer import Customer as CustomerModel

# This router handles all order-related API endpoints
router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

# Endpoint to create a new order
@router.post("/", response_model=Order)
def create_order(request: OrderCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Create a new order.
    If authenticated, associate with the user's customer profile.
    If not, create a guest customer record.
    """
    # Find the customer profile for the logged-in user
    customer = db.query(CustomerModel).filter(CustomerModel.user_id == user.id).first() if user else None
    if customer:
        request.customer_id = customer.id
    return controller.create(db, request)

# Endpoint to get a list of all orders
@router.get("/", response_model=List[Order])
def get_orders(db: Session = Depends(get_db)):
    """
    Get all orders.
    """
    return controller.read_all(db)

# Endpoint to get a single order by its ID
@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get a specific order by ID.
    """
    return controller.read_one(db, order_id)

# Endpoint to update an order by its ID
@router.put("/{order_id}", response_model=Order)
def update_order(
    order_id: int,
    request: OrderUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Update an order's status and other details.
    Records status changes in history.
    """
    return controller.update(db, order_id, request, user)

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
    from api.models.Orders import OrderStatusHistory
    history = db.query(OrderStatusHistory).filter(
        OrderStatusHistory.order_id == order_id
    ).order_by(OrderStatusHistory.changed_at.desc()).all()
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No history found for this order"
        )
    return history
