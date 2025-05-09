from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Menu
from ..schemas.Menu import MenuCreate, MenuUpdate
from sqlalchemy.exc import SQLAlchemyError

# Controller function to create a new menu item
def create(db: Session, request: MenuCreate):
    """
    Create a new menu item.
    """
    new_item = Menu(
        name=request.name,
        description=request.description,
        price=request.price,
        category=request.category,
        dietary=request.dietary
    )
    
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    return new_item

# Controller function to get all menu items
def read_all(db: Session, category=None, dietary=None, min_price=None, max_price=None, name=None):
    """
    Retrieve all menu items with optional filters.
    """
    try:
        query = db.query(Menu)
        if category:
            query = query.filter(Menu.category == category)
        if dietary:
            query = query.filter(Menu.dietary == dietary)
        if min_price is not None:
            query = query.filter(Menu.price >= min_price)
        if max_price is not None:
            query = query.filter(Menu.price <= max_price)
        if name:
            query = query.filter(Menu.name.ilike(f"%{name}%"))
        return query.all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

# Controller function to get a single menu item by ID
def read_one(db: Session, item_id: int):
    """
    Retrieve a single menu item by ID.
    """
    try:
        item = db.query(Menu).filter(Menu.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

# Controller function to update a menu item by ID
def update(db: Session, menu_id: int, request: MenuUpdate):
    """
    Update a menu item by ID.
    """
    try:
        item = db.query(Menu).filter(Menu.id == menu_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
        return item.first()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

# Controller function to delete a menu item by ID
def delete(db: Session, menu_id: int):
    """
    Delete a menu item by ID.
    """
    try:
        item = db.query(Menu).filter(Menu.id == menu_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {"detail": "Menu item deleted"} 