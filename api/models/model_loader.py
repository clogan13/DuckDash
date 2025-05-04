from . import Customer, Feedback, Orders, Promotion, Payment, Menu, Inventory
from ..dependencies.database import engine, Base


def index():
    # Create all tables
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

