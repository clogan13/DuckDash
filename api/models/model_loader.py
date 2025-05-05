# model_loader.py
# This script imports all SQLAlchemy models and creates all tables in the database.
# Run this script to ensure your database schema matches your models.
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from . import Customer, Order, Promotion, Payment, Menu, Inventory
from .user import User
from ..dependencies.database import engine, Base

Base = declarative_base()

def index():
    """Create all tables in the database."""
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
        # Test the connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Connection test result: {result.fetchone()}")
            
    except Exception as e:
        print(f"Error creating database tables: {e}")

def load_models():
    """Load all models into the Base class."""
    # This import will trigger the creation of all models
    pass

__all__ = ['Base', 'load_models']

if __name__ == "__main__":
    index()

