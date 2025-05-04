from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.Ingredient import IngredientCreate, IngredientUpdate, Ingredient
from ..controllers import Ingredient as controller
from typing import List

# This router handles all ingredient-related API endpoints
router = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"]
)

# Endpoint to create a new ingredient
@router.post("/", response_model=Ingredient)
def create_ingredient(request: IngredientCreate, db: Session = Depends(get_db)):
    """Create a new ingredient and return it with its ID."""
    return controller.create(db=db, request=request)

# Endpoint to get a list of all ingredients
@router.get("/", response_model=List[Ingredient])
def get_ingredients(db: Session = Depends(get_db)):
    """Retrieve all ingredients from the database."""
    return controller.read_all(db)

# Endpoint to get a single ingredient by its ID
@router.get("/{ingredient_id}", response_model=Ingredient)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Retrieve an ingredient by its unique ID."""
    return controller.read_one(db, ingredient_id)

# Endpoint to update an ingredient by its ID
@router.put("/{ingredient_id}", response_model=Ingredient)
def update_ingredient(ingredient_id: int, request: IngredientUpdate, db: Session = Depends(get_db)):
    """Update an ingredient's details by its ID."""
    return controller.update(db, ingredient_id, request)

# Endpoint to delete an ingredient by its ID
@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Delete an ingredient by its unique ID."""
    controller.delete(db, ingredient_id)
    return None 