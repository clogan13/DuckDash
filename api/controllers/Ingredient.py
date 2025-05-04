from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Ingredient
from ..schemas.ingredients import IngredientCreate, IngredientUpdate
from sqlalchemy.exc import SQLAlchemyError

# Controller function to create a new ingredient
def create(db: Session, request: IngredientCreate):
    new_item = Ingredient(
        name=request.name,
        unit=request.unit
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item

# Controller function to get all ingredients
def read_all(db: Session):
    return db.query(Ingredient).all()

# Controller function to get a single ingredient by ID
def read_one(db: Session, ingredient_id: int):
    item = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found!")
    return item

# Controller function to update an ingredient by ID
def update(db: Session, ingredient_id: int, request: IngredientUpdate):
    item = db.query(Ingredient).filter(Ingredient.id == ingredient_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found!")
    update_data = request.dict(exclude_unset=True)
    item.update(update_data, synchronize_session=False)
    db.commit()
    return item.first()

# Controller function to delete an ingredient by ID
def delete(db: Session, ingredient_id: int):
    item = db.query(Ingredient).filter(Ingredient.id == ingredient_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found!")
    item.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Ingredient deleted"} 