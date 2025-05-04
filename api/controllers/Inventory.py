from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Inventory
from ..schemas.Inventory import InventoryCreate, InventoryUpdate
from sqlalchemy.exc import SQLAlchemyError

# Controller function to create a new inventory item
def create(db: Session, request: InventoryCreate):
    new_item = Inventory(
        ingredient_id=request.ingredient_id,
        quantity=request.quantity,
        unit_cost=request.unit_cost
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item

# Controller function to get all inventory items
def read_all(db: Session):
    return db.query(Inventory).all()

# Controller function to get a single inventory item by ID
def read_one(db: Session, inventory_id: int):
    item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found!")
    return item

# Controller function to update an inventory item by ID
def update(db: Session, inventory_id: int, request: InventoryUpdate):
    item = db.query(Inventory).filter(Inventory.id == inventory_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found!")
    update_data = request.dict(exclude_unset=True)
    item.update(update_data, synchronize_session=False)
    db.commit()
    return item.first()

# Controller function to delete an inventory item by ID
def delete(db: Session, inventory_id: int):
    item = db.query(Inventory).filter(Inventory.id == inventory_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found!")
    item.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Inventory item deleted"} 