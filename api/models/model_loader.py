# model_loader.py
# This script imports all SQLAlchemy models and creates all tables in the database.
# Run this script to ensure your database schema matches your models.
from . import Customer, Feedback, Order, Promotion, Payment, Menu, Inventory
from .user import User
from ..dependencies.database import engine, Base

def index():
    """
    Create all tables in the database as defined by the SQLAlchemy models.
    Run this function if you need to initialize or update your database schema.
    """
    # Create all tables
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

