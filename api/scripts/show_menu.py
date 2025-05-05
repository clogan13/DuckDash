from api.dependencies.database import SessionLocal
from api.models.Menu import Menu

def show_menu():
    db = SessionLocal()
    try:
        menu_items = db.query(Menu).all()
        print("\nMenu Items:")
        print("-" * 50)
        for item in menu_items:
            print(f"Name: {item.name}")
            print(f"Description: {item.description}")
            print(f"Price: ${item.price}")
            print(f"Category: {item.category}")
            print(f"Dietary: {item.dietary}")
            print("-" * 50)
    finally:
        db.close()

if __name__ == "__main__":
    show_menu() 