from api.dependencies.database import SessionLocal
from api.models.Menu import Menu

def add_menu_items():
    db = SessionLocal()
    try:
        # Menu items to add
        menu_items = [
            {
                "name": "Classic Burger",
                "description": "Juicy beef patty with lettuce, tomato, and special sauce",
                "price": 9.99,
                "category": "Burgers",
                "dietary": "None"
            },
            {
                "name": "Vegan Burger",
                "description": "Plant-based patty with vegan cheese and fresh veggies",
                "price": 10.99,
                "category": "Burgers",
                "dietary": "Vegan"
            },
            {
                "name": "Caesar Salad",
                "description": "Fresh romaine lettuce with Caesar dressing and croutons",
                "price": 8.99,
                "category": "Salads",
                "dietary": "None"
            },
            {
                "name": "Quinoa Bowl",
                "description": "Healthy quinoa with roasted vegetables and tahini dressing",
                "price": 11.99,
                "category": "Salads",
                "dietary": "Vegan"
            },
            {
                "name": "Margherita Pizza",
                "description": "Classic pizza with tomato sauce, mozzarella, and basil",
                "price": 12.99,
                "category": "Pizza",
                "dietary": "Vegetarian"
            },
            {
                "name": "Gluten-Free Pizza",
                "description": "Gluten-free crust with your choice of toppings",
                "price": 13.99,
                "category": "Pizza",
                "dietary": "Gluten-Free"
            },
            {
                "name": "Chocolate Cake",
                "description": "Rich chocolate cake with chocolate ganache",
                "price": 6.99,
                "category": "Desserts",
                "dietary": "None"
            },
            {
                "name": "Vegan Brownie",
                "description": "Fudgy vegan brownie with walnuts",
                "price": 5.99,
                "category": "Desserts",
                "dietary": "Vegan"
            }
        ]
        
        # Add each menu item
        for item in menu_items:
            try:
                menu_item = Menu(**item)
                db.add(menu_item)
                print(f"Successfully added: {item['name']}")
            except Exception as e:
                print(f"Error adding {item['name']}: {str(e)}")
                db.rollback()
        
        db.commit()
        print("\nAll menu items added successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_menu_items() 