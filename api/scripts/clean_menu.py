from api.dependencies.database import SessionLocal
from api.models.Menu import Menu
from sqlalchemy import func

def clean_menu():
    db = SessionLocal()
    try:
        # Find duplicates based on name and category
        duplicates = db.query(Menu.name, Menu.category, func.count('*').label('count'))\
            .group_by(Menu.name, Menu.category)\
            .having(func.count('*') > 1)\
            .all()
        
        for name, category, count in duplicates:
            print(f"Found {count} duplicates for {name} in {category}")
            # Keep the first one and delete the rest
            items = db.query(Menu)\
                .filter(Menu.name == name, Menu.category == category)\
                .order_by(Menu.id)\
                .all()
            
            # Keep the first one, delete the rest
            for item in items[1:]:
                print(f"Deleting duplicate: {item.name} (ID: {item.id})")
                db.delete(item)
        
        db.commit()
        print("\nMenu cleaned successfully!")
    except Exception as e:
        print(f"Error cleaning menu: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_menu() 