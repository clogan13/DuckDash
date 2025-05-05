import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"
USER_EMAIL = "testuser@example.com"
USER_PASSWORD = "password123"

@pytest.mark.order(1)
def test_register_user():
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": USER_EMAIL,
        "password": USER_PASSWORD,
        "phone": "555-0000"
    }
    r = requests.post(f"{BASE_URL}/auth/register", json=data)
    assert r.status_code in (200, 400)  # 400 if already registered

@pytest.mark.order(2)
def test_login_user():
    data = {
        "username": USER_EMAIL,
        "password": USER_PASSWORD
    }
    r = requests.post(f"{BASE_URL}/auth/login", data=data)
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token
    global AUTH_TOKEN
    AUTH_TOKEN = token

@pytest.mark.order(3)
def test_seed_menu():
    # Add a menu item if not present
    r = requests.get(f"{BASE_URL}/menu/")
    menu = r.json()
    if not any(item["name"] == "Test Burger" for item in menu):
        data = {
            "name": "Test Burger",
            "description": "A seeded test burger.",
            "price": 9.99,
            "category": "Burgers",
            "dietary": "None"
        }
        r = requests.post(f"{BASE_URL}/menu/", json=data, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        assert r.status_code == 200

@pytest.mark.order(4)
def test_place_order():
    # Get menu item id
    r = requests.get(f"{BASE_URL}/menu/")
    menu = r.json()
    burger = next((item for item in menu if item["name"] == "Test Burger"), None)
    assert burger is not None
    order_data = {
        "order_details": [
            {"menu_item_id": burger["id"], "quantity": 2}
        ]
    }
    r = requests.post(f"{BASE_URL}/orders/", json=order_data, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
    assert r.status_code == 200
    order = r.json()
    assert "id" in order or "order_id" in order
    print("Order placed!", order) 