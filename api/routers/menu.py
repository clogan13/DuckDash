from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.Menu import MenuCreate, MenuUpdate, Menu
from ..controllers import Menu as controller
from typing import List

# This router handles all menu item-related API endpoints
router = APIRouter(
    prefix="/menu",
    tags=["menu"]
)

# Endpoint to create a new menu item
@router.post("/", response_model=Menu)
def create_menu(request: MenuCreate, db: Session = Depends(get_db)):
    """Create a new menu item and return it with its ID."""
    return controller.create(db=db, request=request)

# Endpoint to get a list of all menu items
@router.get("/", response_model=List[Menu])
def get_menus(
    category: str = Query(None, description="Filter by category"),
    dietary: str = Query(None, description="Filter by dietary info"),
    min_price: float = Query(None, description="Minimum price"),
    max_price: float = Query(None, description="Maximum price"),
    name: str = Query(None, description="Search by name"),
    db: Session = Depends(get_db)
):
    """Retrieve all menu items from the database, with optional filters."""
    return controller.read_all(db, category, dietary, min_price, max_price, name)

# Endpoint to get a single menu item by its ID
@router.get("/{menu_id}", response_model=Menu)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """Retrieve a menu item by its unique ID."""
    return controller.read_one(db, menu_id)

# Endpoint to update a menu item by its ID
@router.put("/{menu_id}", response_model=Menu)
def update_menu(menu_id: int, request: MenuUpdate, db: Session = Depends(get_db)):
    """Update a menu item's details by its ID."""
    return controller.update(db, menu_id, request)

# Endpoint to delete a menu item by its ID
@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """Delete a menu item by its unique ID."""
    controller.delete(db, menu_id)
    return None 