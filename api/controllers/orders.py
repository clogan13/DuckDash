"""
Controller for order operations.
Handles creation, retrieval, update, and deletion of orders and their items.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import Orders as model
from ..models.Menu import Menu, menu_item_ingredient
from ..schemas.orders import OrderCreate, OrderUpdate
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from ..dependencies.auth import get_current_user
from ..models.Inventory import Inventory
from sqlalchemy import select

# Controller function to create a new order in the database, including order items
def create(db: Session, request: OrderCreate):
    """
    Create a new order and its associated order items.
    If customer_id is not provided, create a guest customer record.
    Calculates the total amount and validates menu items.
    Deducts inventory for each ingredient used in the order.
    """
    # If no customer_id, create a guest customer
    if not request.customer_id:
        from ..models.Customer import Customer
        guest = Customer(
            first_name=request.first_name or "Guest",
            last_name=request.last_name or "",
            phone=request.phone,
            email=request.email,
            address=request.address
        )
        db.add(guest)
        db.commit()
        db.refresh(guest)
        customer_id = guest.id
    else:
        customer_id = request.customer_id

    total_amount = 0
    order_items = []
    ingredient_deductions = {}  # {ingredient_id: total_to_deduct}
    for detail in request.order_details:
        menu_item = db.query(Menu).filter(Menu.id == detail.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item {detail.menu_item_id} not found!")
        item_price = menu_item.price * detail.quantity
        total_amount += item_price
        order_items.append(model.OrderItem(
            menu_item_id=detail.menu_item_id,
            quantity=detail.quantity,
            item_price=menu_item.price
        ))
        # Inventory deduction logic (fixed)
        ingredient_rows = db.execute(
            menu_item_ingredient.select().where(
                menu_item_ingredient.c.menu_item_id == detail.menu_item_id
            )
        ).fetchall()
        for row in ingredient_rows:
            ingredient_id = row.ingredient_id
            required_qty = row.quantity
            total_required = required_qty * detail.quantity
            ingredient_deductions[ingredient_id] = ingredient_deductions.get(ingredient_id, 0) + total_required
    # Check and deduct inventory
    try:
        for ingredient_id, total_to_deduct in ingredient_deductions.items():
            inventory = db.query(Inventory).filter(Inventory.ingredient_id == ingredient_id).with_for_update().first()
            if not inventory or inventory.quantity < total_to_deduct:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient inventory for ingredient {ingredient_id}")
            inventory.quantity -= total_to_deduct
        db.commit()
    except Exception as e:
        db.rollback()
        raise
    new_order = model.Order(
        customer_id=customer_id,
        tracking_number=request.tracking_number,
        status=request.status,
        order_time=datetime.utcnow(),
        wait_time_minutes=request.wait_time_minutes,
        total_amount=total_amount,
        items=order_items
    )
    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        # Record initial status in history
        history_entry = model.OrderStatusHistory(
            order_id=new_order.id,
            status=request.status,
            changed_at=datetime.utcnow(),
            notes="Order created"
        )
        db.add(history_entry)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_order

# Controller function to get all orders from the database
def read_all(db: Session):
    """
    Retrieve all orders from the database.
    """
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

# Controller function to get a single order by ID
def read_one(db: Session, order_id: int):
    """
    Retrieve a single order by its ID.
    """
    try:
        item = db.query(model.Order).filter(model.Order.id == order_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

# Controller function to update an order by ID
def update(db: Session, order_id: int, request: OrderUpdate, current_user = None):
    """
    Update an existing order by its ID.
    Records status changes in history.
    """
    try:
        item = db.query(model.Order).filter(model.Order.id == order_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
        
        # Get current order
        current_order = item.first()
        
        # Check if status is being updated
        if request.status and request.status != current_order.status:
            # Record status change in history
            history_entry = model.OrderStatusHistory(
                order_id=order_id,
                status=request.status,
                changed_at=datetime.utcnow(),
                changed_by=current_user.id if current_user else None,
                notes=request.notes
            )
            db.add(history_entry)
        
        # Update order
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
        
        # Return updated order
        return item.first()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

# Controller function to delete an order by ID
def delete(db: Session, order_id: int):
    """
    Delete an order by its ID.
    """
    try:
        item = db.query(model.Order).filter(model.Order.id == order_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
