from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.Inventory import InventoryCreate, InventoryUpdate, Inventory
from ..controllers import Inventory as controller
from typing import List

# This router handles all inventory-related API endpoints
router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)

# Endpoint to create a new inventory item
@router.post("/", response_model=Inventory)
def create_inventory(request: InventoryCreate, db: Session = Depends(get_db)):
    """Create a new inventory item and return it with its ID."""
    return controller.create(db=db, request=request)

# Endpoint to get a list of all inventory items
@router.get("/", response_model=List[Inventory])
def get_inventories(db: Session = Depends(get_db)):
    """Retrieve all inventory items from the database."""
    return controller.read_all(db)

# Endpoint to get a single inventory item by its ID
@router.get("/{inventory_id}", response_model=Inventory)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    """Retrieve an inventory item by its unique ID."""
    return controller.read_one(db, inventory_id)

# Endpoint to update an inventory item by its ID
@router.put("/{inventory_id}", response_model=Inventory)
def update_inventory(inventory_id: int, request: InventoryUpdate, db: Session = Depends(get_db)):
    """Update an inventory item's details by its ID."""
    return controller.update(db, inventory_id, request)

# Endpoint to delete an inventory item by its ID
@router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    """Delete an inventory item by its unique ID."""
    controller.delete(db, inventory_id)
    return None 