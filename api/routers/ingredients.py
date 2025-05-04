"""
Router for ingredient-related endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import ingredients as controller
from ..schemas.ingredients import IngredientCreate, IngredientUpdate

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)

@router.get("/")
def get_ingredients(db: Session = Depends(get_db)):
    """
    Get all ingredients.
    """
    return controller.read_all(db)

@router.post("/")
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    """
    Create a new ingredient.
    """
    return controller.create(db, ingredient)

@router.get("/{ingredient_id}")
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """
    Get a specific ingredient by ID.
    """
    return controller.read_one(db, ingredient_id)

@router.put("/{ingredient_id}")
def update_ingredient(ingredient_id: int, ingredient: IngredientUpdate, db: Session = Depends(get_db)):
    """
    Update an existing ingredient.
    """
    return controller.update(db, ingredient_id, ingredient)

@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """
    Delete an ingredient.
    """
    return controller.delete(db, ingredient_id) 