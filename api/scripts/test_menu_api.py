import requests

def test_menu_api():
    try:
        response = requests.get("http://localhost:8000/menu/")
        if response.status_code == 200:
            menu_items = response.json()
            print(f"Successfully retrieved {len(menu_items)} menu items:")
            for item in menu_items:
                print(f"ID: {item['id']}, Name: {item['name']}, Category: {item['category']}, Price: ${item['price']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error testing menu API: {str(e)}")

if __name__ == "__main__":
    test_menu_api() 