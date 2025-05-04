import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.models.Orders import OrderStatus

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to DuckDash API"}

def test_create_menu():
    menu_data = {
        "name": "Test Burger",
        "description": "A delicious test burger",
        "price": 9.99,
        "category": "Burgers",
        "dietary": "None"
    }
    response = client.post("/menu/", json=menu_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == menu_data["name"]
    assert data["price"] == menu_data["price"]
    return data["id"]

def test_create_inventory():
    # First create an ingredient
    ingredient_data = {
        "name": "Test Ingredient",
        "unit": "pieces",
        "category": "Test Category"
    }
    ingredient_response = client.post("/ingredients/", json=ingredient_data)
    assert ingredient_response.status_code == 200
    ingredient_id = ingredient_response.json()["id"]

    inventory_data = {
        "ingredient_id": ingredient_id,
        "quantity": 100.0,
        "unit_cost": 1.99
    }
    response = client.post("/inventory/", json=inventory_data)
    assert response.status_code == 200
    data = response.json()
    assert data["ingredient_id"] == ingredient_id
    assert data["quantity"] == inventory_data["quantity"]
    return data["id"]

def test_create_order():
    # First create a customer
    customer_data = {
        "first_name": "Test",
        "last_name": "Customer",
        "email": "test@example.com",
        "phone": "123-456-7890",
        "address": "123 Test St"
    }
    customer_response = client.post("/customers/", json=customer_data)
    assert customer_response.status_code == 200
    customer_id = customer_response.json()["id"]

    # Create a menu item
    menu_id = test_create_menu()

    order_data = {
        "customer_id": customer_id,
        "tracking_number": "TEST123",
        "status": OrderStatus.pending.value,
        "total_amount": 19.98,
        "order_details": [
            {
                "menu_item_id": menu_id,
                "quantity": 2,
                "item_price": 9.99
            }
        ]
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
    return data["id"]

def test_create_order_detail():
    # First create a menu item and order
    menu_id = test_create_menu()
    order_id = test_create_order()
    
    order_detail_data = {
        "order_id": order_id,
        "menu_item_id": menu_id,
        "quantity": 2,
        "item_price": 9.99
    }
    response = client.post("/order-details/", json=order_detail_data)
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == order_id
    assert data["menu_item_id"] == menu_id
    assert data["quantity"] == order_detail_data["quantity"] 