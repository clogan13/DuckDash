from api.dependencies.database import SessionLocal
from api.models.Menu import Menu
from decimal import Decimal
from sqlalchemy import func

def clean_and_seed():
    db = SessionLocal()
    try:
        print("Cleaning up duplicate menu items...")
        # Find all duplicates
        duplicates = db.query(Menu.name, Menu.category, func.count('*').label('count'))\
            .group_by(Menu.name, Menu.category)\
            .having(func.count('*') > 1)\
            .all()
        
        for name, category, count in duplicates:
            print(f"Found {count} duplicates for {name} in {category}")
            # Keep the first one, delete the rest
            items = db.query(Menu)\
                .filter(Menu.name == name, Menu.category == category)\
                .order_by(Menu.id)\
                .all()
            
            # Keep the first one, delete the rest
            for item in items[1:]:
                print(f"Deleting duplicate: {item.name} (ID: {item.id})")
                db.delete(item)
        
        db.commit()
        print("\nDuplicates cleaned up!")
        
        print("\nAdding menu items...")
        # Fresh menu items
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

        # Add menu items if they don't exist
        for item in menu_items:
            existing = db.query(Menu)\
                .filter(Menu.name == item["name"], Menu.category == item["category"])\
                .first()
            
            if not existing:
                menu_item = Menu(**item)
                db.add(menu_item)
                print(f"Added: {item['name']}")
            else:
                print(f"Skipped (already exists): {item['name']}")
        
        db.commit()
        print("\nMenu items added successfully!")
        
        # Verify final menu items
        print("\nCurrent menu items:")
        all_items = db.query(Menu).order_by(Menu.category, Menu.name).all()
        for item in all_items:
            print(f"ID: {item.id}, Name: {item.name}, Category: {item.category}, Price: ${item.price}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_and_seed() 