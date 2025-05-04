-- Check all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Check menu table
SELECT * FROM menu;

-- Check inventory table
SELECT * FROM inventory;

-- Check orders table
SELECT * FROM orders;

-- Check order_details table
SELECT * FROM order_details;

-- Check ingredients table
SELECT * FROM ingredients;

-- Check menu_ingredients table
SELECT * FROM menu_ingredients; 