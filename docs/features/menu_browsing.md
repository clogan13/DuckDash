# Menu Browsing Feature Documentation

## Overview
The menu browsing feature allows users (both authenticated and unauthenticated) to view and filter menu items. While viewing menu items is public, modifying menu items (create, update, delete) requires authentication.

## Endpoints

### Public Endpoints

#### 1. Get All Menu Items
```http
GET /menu/
```
Retrieves all menu items with optional filtering.

**Query Parameters:**
- `category` (string, optional): Filter by menu category (e.g., "Burgers", "Salads")
- `dietary` (string, optional): Filter by dietary restrictions (e.g., "Vegan", "Gluten-Free")
- `min_price` (float, optional): Minimum price filter
- `max_price` (float, optional): Maximum price filter
- `name` (string, optional): Search by menu item name (case-insensitive)

**Response Example:**
```json
[
  {
    "id": 1,
    "name": "Classic Burger",
    "description": "Juicy beef patty with lettuce, tomato, and special sauce",
    "price": 9.99,
    "category": "Burgers",
    "dietary": "None"
  }
]
```

#### 2. Get Single Menu Item
```http
GET /menu/{menu_id}
```
Retrieves a specific menu item by ID.

### Protected Endpoints (Requires Authentication)

#### 1. Create Menu Item
```http
POST /menu/
```
Creates a new menu item.

**Request Body:**
```json
{
  "name": "string",
  "description": "string",
  "price": 0,
  "category": "string",
  "dietary": "string"
}
```

#### 2. Update Menu Item
```http
PUT /menu/{menu_id}
```
Updates an existing menu item.

#### 3. Delete Menu Item
```http
DELETE /menu/{menu_id}
```
Deletes a menu item.

## Implementation Details

### Authentication
- Menu browsing (GET endpoints) is public and requires no authentication
- Menu modification (POST, PUT, DELETE) requires JWT authentication
- Authentication is implemented using FastAPI's dependency injection system

### Code Structure

#### Router (`api/routers/menu.py`)
- Defines all menu-related endpoints
- Implements filtering logic through query parameters
- Handles authentication requirements

#### Controller (`api/controllers/Menu.py`)
- Contains business logic for menu operations
- Implements database queries and filtering
- Handles error cases and edge conditions

#### Model (`api/models/Menu.py`)
- SQLAlchemy model defining the menu item structure
- Maps to the database table

### Sample Data
The feature includes a seeding script (`api/scripts/seed_menu.py`) that populates the database with sample menu items across different categories:

- Burgers (Classic, Vegan)
- Salads (Caesar, Quinoa Bowl)
- Pizza (Margherita, Gluten-Free)
- Desserts (Chocolate Cake, Vegan Brownie)

## Testing
Tests are implemented in `tests/test_api.py` and cover:
- Menu item creation
- Menu browsing with various filters
- Authentication requirements
- Error cases

## Usage Examples

### Filter by Category
```http
GET /menu/?category=Burgers
```

### Filter by Dietary Restriction
```http
GET /menu/?dietary=Vegan
```

### Price Range Filter
```http
GET /menu/?min_price=10&max_price=15
```

### Name Search
```http
GET /menu/?name=salad
```

### Combined Filters
```http
GET /menu/?category=Salads&dietary=Vegan&max_price=12
```

## Error Handling
- Invalid menu IDs return 404 Not Found
- Unauthorized modifications return 401 Unauthorized
- Invalid filter values return appropriate 400 Bad Request errors

## Future Enhancements
Potential improvements for future iterations:
1. Advanced search capabilities (fuzzy matching, multiple categories)
2. Additional filtering options (availability, popularity)
3. Sorting options (price, name, popularity)
4. Pagination for large menu sets
5. Image support for menu items 