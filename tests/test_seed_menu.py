import requests

API_URL = "http://127.0.0.1:8000/menu/"

MENU_ITEMS = [
    {"name": "Burger", "description": "Juicy beef burger with lettuce and tomato", "price": 8.99, "category": "Entree"},
    {"name": "Fries", "description": "Crispy golden fries", "price": 3.49, "category": "Side"},
    {"name": "Chicken Sandwich", "description": "Grilled chicken breast with pickles", "price": 7.99, "category": "Entree"},
    {"name": "Caesar Salad", "description": "Fresh romaine, parmesan, and croutons", "price": 6.49, "category": "Salad"},
    {"name": "Soda", "description": "Choice of Coke, Sprite, or Fanta", "price": 1.99, "category": "Drink"},
    {"name": "Milkshake", "description": "Vanilla, chocolate, or strawberry", "price": 4.49, "category": "Dessert"},
    {"name": "Fish Tacos", "description": "Three tacos with crispy fish and slaw", "price": 9.99, "category": "Entree"},
    {"name": "Mozzarella Sticks", "description": "Fried cheese sticks with marinara", "price": 5.99, "category": "Appetizer"},
    {"name": "Veggie Wrap", "description": "Grilled veggies in a spinach wrap", "price": 7.49, "category": "Entree"},
    {"name": "Brownie", "description": "Fudgy chocolate brownie", "price": 2.99, "category": "Dessert"},
]

def test_seed_menu():
    for item in MENU_ITEMS:
        resp = requests.post(API_URL, json=item)
        assert resp.status_code in (200, 201), f"Failed to add {item['name']}: {resp.text}"
    print("Menu seeded successfully!") 