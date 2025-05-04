from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.customers import CustomerCreate, CustomerUpdate, Customer
from ..controllers import Customer as controller
from typing import List

# This router handles all customer-related API endpoints
router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

# Endpoint to create a new customer
@router.post("/", response_model=Customer)
def create_customer(request: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer and return it with its ID."""
    return controller.create(db=db, request=request)

# Endpoint to get a list of all customers
@router.get("/", response_model=List[Customer])
def get_customers(db: Session = Depends(get_db)):
    """Retrieve all customers from the database."""
    return controller.read_all(db)

# Endpoint to get a single customer by their ID
@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Retrieve a customer by their unique ID."""
    return controller.read_one(db, customer_id)

@router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, request: CustomerUpdate, db: Session = Depends(get_db)):
    """Update a customer's details by their ID."""
    return controller.update(db, customer_id, request)

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete a customer by their unique ID."""
    controller.delete(db, customer_id)
    return None 