# model_loader.py
# This script imports all SQLAlchemy models and creates all tables in the database.
# Run this script to ensure your database schema matches your models.
from sqlalchemy import text
from . import Customer, Feedback, Order, Promotion, Payment, Menu, Inventory
from .user import User
from ..dependencies.database import engine, Base

def index():
    """
    Create all database tables.
    """
    try:
        # Drop tables in correct order to handle foreign key constraints
        with engine.connect() as conn:
            # Disable foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # Drop all tables
            Base.metadata.drop_all(bind=engine)
            
            # Re-enable foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
            # Recreate all tables
            Base.metadata.create_all(bind=engine)
            
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")

