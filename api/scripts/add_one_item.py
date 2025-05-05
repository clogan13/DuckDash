from api.dependencies.database import SessionLocal
from api.models.Menu import Menu
from decimal import Decimal

def add_burger():
    db = SessionLocal()
    try:
        # Create a single burger
        burger = Menu(
            name="Classic Burger",
            description="Juicy beef patty with lettuce, tomato, and special sauce",
            price=Decimal("9.99"),
            category="Burgers",
            dietary="None"
        )
        
        db.add(burger)
        db.commit()
        print("Successfully added Classic Burger!")
        
        # Verify it was added
        burgers = db.query(Menu).filter(Menu.name == "Classic Burger").all()
        print(f"\nFound {len(burgers)} burgers in database:")
        for b in burgers:
            print(f"ID: {b.id}, Name: {b.name}, Price: ${b.price}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_burger() 