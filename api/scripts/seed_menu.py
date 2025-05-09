"""
Script to seed the database with sample menu items.
Run this script to populate the menu with test data.
"""
from sqlalchemy.orm import Session
from ..dependencies.database import SessionLocal
from ..models.Menu import Menu
from decimal import Decimal

def seed_menu():
    db = SessionLocal()
    try:
        # Sample menu items
        menu_items = [
            {
                "name": "Classic Burger",
                "description": "Juicy beef patty with lettuce, tomato, and special sauce",
                "price": Decimal("9.99"),
                "category": "Burgers",
                "dietary": "None"
            },
            {
                "name": "Vegan Burger",
                "description": "Plant-based patty with vegan cheese and fresh veggies",
                "price": Decimal("10.99"),
                "category": "Burgers",
                "dietary": "Vegan"
            },
            {
                "name": "Caesar Salad",
                "description": "Fresh romaine lettuce with Caesar dressing and croutons",
                "price": Decimal("8.99"),
                "category": "Salads",
                "dietary": "None"
            },
            {
                "name": "Quinoa Bowl",
                "description": "Healthy quinoa with roasted vegetables and tahini dressing",
                "price": Decimal("11.99"),
                "category": "Salads",
                "dietary": "Vegan"
            },
            {
                "name": "Margherita Pizza",
                "description": "Classic pizza with tomato sauce, mozzarella, and basil",
                "price": Decimal("12.99"),
                "category": "Pizza",
                "dietary": "Vegetarian"
            },
            {
                "name": "Gluten-Free Pizza",
                "description": "Gluten-free crust with your choice of toppings",
                "price": Decimal("13.99"),
                "category": "Pizza",
                "dietary": "Gluten-Free"
            },
            {
                "name": "Chocolate Cake",
                "description": "Rich chocolate cake with chocolate ganache",
                "price": Decimal("6.99"),
                "category": "Desserts",
                "dietary": "None"
            },
            {
                "name": "Vegan Brownie",
                "description": "Fudgy vegan brownie with walnuts",
                "price": Decimal("5.99"),
                "category": "Desserts",
                "dietary": "Vegan"
            }
        ]

        # Add menu items to database if they don't exist
        for item in menu_items:
            existing_item = db.query(Menu).filter(
                Menu.name == item["name"],
                Menu.category == item["category"]
            ).first()
            
            if not existing_item:
                menu_item = Menu(**item)
                db.add(menu_item)
                print(f"Added: {item['name']}")
            else:
                print(f"Skipped (already exists): {item['name']}")
        
        db.commit()
        print("Successfully seeded menu items!")
    except Exception as e:
        print(f"Error seeding menu items: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_menu() 