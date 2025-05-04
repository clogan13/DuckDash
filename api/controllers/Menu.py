from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Menu
from ..schemas.Menu import MenuCreate, MenuUpdate
from sqlalchemy.exc import SQLAlchemyError

# Controller function to create a new menu item
def create(db: Session, request: MenuCreate):
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
def read_all(db: Session):
    return db.query(Menu).all()

# Controller function to get a single menu item by ID
def read_one(db: Session, menu_id: int):
    item = db.query(Menu).filter(Menu.id == menu_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")
    return item

# Controller function to update a menu item by ID
def update(db: Session, menu_id: int, request: MenuUpdate):
    item = db.query(Menu).filter(Menu.id == menu_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")
    update_data = request.dict(exclude_unset=True)
    item.update(update_data, synchronize_session=False)
    db.commit()
    return item.first()

# Controller function to delete a menu item by ID
def delete(db: Session, menu_id: int):
    item = db.query(Menu).filter(Menu.id == menu_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")
    item.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Menu item deleted"} 