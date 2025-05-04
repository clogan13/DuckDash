# DuckDash Promotion System Documentation

## Overview
The promotion system allows for the creation, management, and application of promotional codes to orders. It supports various types of discounts and includes validation mechanisms to ensure proper usage.

## Database Schema

### Promotion Table
```sql
CREATE TABLE promotions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    discount_type ENUM('percentage', 'fixed_amount') NOT NULL,
    discount_value DECIMAL(10,2) NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    usage_limit INT,
    current_usage INT DEFAULT 0,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## API Endpoints

### 1. Create Promotion
- **Endpoint:** `POST /promotions/`
- **Description:** Creates a new promotion
- **Request Body:**
  ```json
  {
    "code": "SUMMER20",
    "discount_type": "percentage",
    "discount_value": 20.00,
    "start_date": "2024-06-01T00:00:00",
    "end_date": "2024-08-31T23:59:59",
    "usage_limit": 100,
    "description": "Summer special 20% off"
  }
  ```

### 2. Get All Promotions
- **Endpoint:** `GET /promotions/`
- **Description:** Retrieves all active promotions
- **Query Parameters:**
  - `active_only`: boolean (optional) - Filter for active promotions only

### 3. Get Promotion by ID
- **Endpoint:** `GET /promotions/{promotion_id}`
- **Description:** Retrieves a specific promotion by ID

### 4. Update Promotion
- **Endpoint:** `PUT /promotions/{promotion_id}`
- **Description:** Updates an existing promotion
- **Request Body:** Same as create promotion

### 5. Delete Promotion
- **Endpoint:** `DELETE /promotions/{promotion_id}`
- **Description:** Deletes a promotion

### 6. Validate Promotion Code
- **Endpoint:** `GET /promotions/validate/{code}`
- **Description:** Validates a promotion code
- **Response:**
  ```json
  {
    "is_valid": true,
    "discount_type": "percentage",
    "discount_value": 20.00,
    "message": "Promotion code is valid"
  }
  ```

## Integration with Orders

### Applying Promotions to Orders
Promotions can be applied during order creation by including the promotion code in the order request:

```json
{
  "customer_id": 1,
  "items": [...],
  "promotion_code": "SUMMER20"
}
```

### Validation Rules
1. **Date Validation:**
   - Promotion must be within its start and end dates
   - Current date must be between start_date and end_date

2. **Usage Limit:**
   - If usage_limit is set, current_usage must be less than usage_limit
   - current_usage is automatically incremented when a promotion is successfully applied

3. **Discount Types:**
   - Percentage discounts: Applied as a percentage of the total order amount
   - Fixed amount discounts: Applied as a fixed amount reduction

## Error Handling

The system handles various error cases:
- Invalid promotion code
- Expired promotion
- Usage limit exceeded
- Invalid discount values
- Date range conflicts

## Implementation Details

### Key Files Modified
1. `api/routers/promotions.py` - New router for promotion endpoints
2. `api/models/Promotion.py` - Promotion model definition
3. `api/schemas/Promotion.py` - Pydantic schemas for promotion requests/responses
4. `api/controllers/orders.py` - Updated to handle promotion application
5. `api/main.py` - Added promotion router to FastAPI app
6. `api/routers/index.py` - Updated router imports

### Database Changes
- Added `description` column to promotions table
- Updated promotion model to include description field
- Added validation logic for promotion codes

## Testing

The promotion system can be tested using the following steps:

1. Create a new promotion:
   ```bash
   curl -X POST "http://localhost:8000/promotions/" \
        -H "Content-Type: application/json" \
        -d '{"code":"TEST20","discount_type":"percentage","discount_value":20.00,"start_date":"2024-01-01T00:00:00","end_date":"2024-12-31T23:59:59","usage_limit":100,"description":"Test promotion"}'
   ```

2. Validate a promotion code:
   ```bash
   curl "http://localhost:8000/promotions/validate/TEST20"
   ```

3. Create an order with a promotion:
   ```bash
   curl -X POST "http://localhost:8000/orders/" \
        -H "Content-Type: application/json" \
        -d '{"customer_id":1,"items":[{"menu_item_id":1,"quantity":2}],"promotion_code":"TEST20"}'
   ```

## Security Considerations

1. Promotion codes are case-sensitive
2. Only active promotions can be applied to orders
3. Usage limits are strictly enforced
4. Date validation prevents expired promotions from being used

## Future Enhancements

Potential improvements for the promotion system:
1. Add support for minimum order amount requirements
2. Implement category-specific promotions
3. Add support for multiple promotions per order
4. Create promotion analytics and reporting
5. Add bulk promotion creation/management 