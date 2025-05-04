from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.Customer import Customer
from ..schemas.customers import CustomerCreate, CustomerUpdate
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Controller function to create a new customer in the database
def create(db: Session, request: CustomerCreate):
    """Create a new customer in the database."""
    new_customer = Customer(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone=request.phone,
        address=request.address,
        created_at=datetime.utcnow()
    )
    try:
        db.add(new_customer)  # Add the new customer to the session
        db.commit()           # Commit the transaction
        db.refresh(new_customer)  # Refresh to get the new ID
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_customer

# Controller function to get all customers from the database
def read_all(db: Session):
    """Retrieve all customers from the database."""
    return db.query(Customer).all()

# Controller function to get a single customer by ID
def read_one(db: Session, customer_id: int):
    """Retrieve a single customer by ID."""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found!")
    return customer

def update(db: Session, customer_id: int, request: CustomerUpdate):
    """Update a customer's details."""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found!")
    
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(customer, key, value)
    
    db.commit()
    db.refresh(customer)
    return customer

def delete(db: Session, customer_id: int):
    """Delete a customer from the database."""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found!")
    db.delete(customer)
    db.commit() 