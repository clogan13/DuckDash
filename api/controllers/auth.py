"""
Authentication controller for user registration and login.
Handles user sign-up and login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models.user import User
from ..models.Customer import Customer
from ..schemas.auth import UserCreate, UserResponse, UserLogin
from ..dependencies.auth import get_password_hash, verify_password

# Create a router for authentication endpoints
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Checks if the email is already registered.
    - Creates a new customer record.
    - Creates a new user record for authentication.
    Returns the created user (without password).
    """
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new customer
    new_customer = Customer(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        address=user.address
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    # Create new user for authentication
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return user information if credentials are correct.
    """
    # Verify user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return db_user 