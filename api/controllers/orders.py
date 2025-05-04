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
from ..models.Promotion import Promotion
from sqlalchemy import func

# Controller function to create a new order in the database, including order items
def create(db: Session, request: OrderCreate):
    """
    Create a new order and its associated order items.
    If customer_id is not provided, create a guest customer record.
    Calculates the total amount and validates menu items.
    Deducts inventory for each ingredient used in the order.
    Applies promotion code if provided.
    """
    # If no customer_id, create a guest customer
    if not request.customer_id:
        from ..models.Customer import Customer
        guest = Customer(
            first_name=request.first_name or "Guest",
            last_name=request.last_name or "",
            phone=request.phone,
            email=request.email,
            address=request.address,
            created_at=datetime.utcnow()
        )
        db.add(guest)
        db.commit()
        db.refresh(guest)
        customer_id = guest.id
    else:
        customer_id = request.customer_id

    # Calculate total amount and validate menu items
    total_amount = 0
    order_items = []
    ingredient_deductions = {}

    for detail in request.order_details:
        menu_item = db.query(Menu).filter(Menu.id == detail.menu_item_id).first()
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item {detail.menu_item_id} not found"
            )
        
        # Calculate item total
        item_total = float(menu_item.price) * detail.quantity
        total_amount += item_total

        # Create order item
        order_item = model.OrderItem(
            menu_item_id=detail.menu_item_id,
            quantity=detail.quantity,
            item_price=menu_item.price
        )
        order_items.append(order_item)

        # Track ingredient deductions
        for ingredient in menu_item.ingredients:
            if ingredient.id not in ingredient_deductions:
                ingredient_deductions[ingredient.id] = 0
            ingredient_deductions[ingredient.id] += float(ingredient.quantity) * detail.quantity

    # Apply promotion if provided
    discount_amount = 0
    if request.promotion_code:
        promo = db.query(Promotion).filter(
            func.lower(Promotion.code) == request.promotion_code.lower()
        ).first()
        now = datetime.utcnow().date()
        
        if not promo:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid promotion code.")
        if promo.start_date > now or promo.end_date < now:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promotion code is not active.")
        if promo.usage_limit is not None and promo.usage_limit <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promotion code usage limit reached.")
        
        # Apply discount
        if promo.discount_percent:
            discount_amount = float(total_amount) * float(promo.discount_percent) / 100.0
        elif promo.discount_amount:
            discount_amount = float(promo.discount_amount)
        
        total_amount = max(0, float(total_amount) - discount_amount)
        
        # Decrement usage_limit if applicable
        if promo.usage_limit is not None:
            promo.usage_limit -= 1

    # Create the order
    new_order = model.Order(
        customer_id=customer_id,
        tracking_number=request.tracking_number,
        status=request.status,
        total_amount=total_amount,
        wait_time_minutes=request.wait_time_minutes,
        promotion_code=request.promotion_code,
        discount_amount=discount_amount,
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
        db.rollback()
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
