from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import Orders as model
from ..models.Menu import Menu
from ..schemas.orders import OrderCreate, OrderUpdate
from sqlalchemy.exc import SQLAlchemyError

# Controller function to create a new order in the database, including order details
def create(db: Session, request: OrderCreate):
    # Calculate total amount and create order items
    total_amount = 0
    order_items = []
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
    new_order = model.Order(
        customer_id=request.customer_id,
        description=request.description,
        total_amount=total_amount,
        items=order_items
    )
    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_order

# Controller function to get all orders from the database
def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

# Controller function to get a single order by ID
def read_one(db: Session, order_id: int):
    try:
        item = db.query(model.Order).filter(model.Order.id == order_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

# Controller function to update an order by ID
def update(db: Session, order_id: int, request: OrderUpdate):
    try:
        item = db.query(model.Order).filter(model.Order.id == order_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

# Controller function to delete an order by ID
def delete(db: Session, order_id: int):
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
