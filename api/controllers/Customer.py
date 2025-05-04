from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import Customer
from ..schemas.Customer import CustomerCreate
from sqlalchemy.exc import SQLAlchemyError

# Controller function to create a new customer in the database
def create(db: Session, request: CustomerCreate):
    new_customer = Customer(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone=request.phone,
        address=request.address
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
    return db.query(Customer).all()

# Controller function to get a single customer by ID
def read_one(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found!")
    return customer 