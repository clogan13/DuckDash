from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.Customer import CustomerCreate, Customer
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
    """Create a new customer and return the created customer with its ID."""
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