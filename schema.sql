-- Create the database
CREATE DATABASE IF NOT EXISTS `Duckdash`
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
USE `Duckdash`;

-- Customers (guests)
CREATE TABLE `customer` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(20),
  `email` VARCHAR(255),
  `address` VARCHAR(255),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Promotions
CREATE TABLE `promotion` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `code` VARCHAR(50) UNIQUE NOT NULL,
  `discount_amount` DECIMAL(10,2) DEFAULT NULL,
  `discount_percent` DECIMAL(5,2) DEFAULT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `usage_limit` INT DEFAULT NULL
) ENGINE=InnoDB;

-- Menu items
CREATE TABLE `menu_item` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(150) NOT NULL,
  `description` TEXT,
  `price` DECIMAL(10,2) NOT NULL,
  `category` VARCHAR(50),
  `dietary` VARCHAR(50),
  `promotion_id` INT DEFAULT NULL,
  FOREIGN KEY (`promotion_id`) REFERENCES `promotion`(`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB;

-- Ingredients
CREATE TABLE `ingredient` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `unit` VARCHAR(50)
) ENGINE=InnoDB;

-- Menu‐Item ⇄ Ingredient (many‐to‐many)
CREATE TABLE `menu_item_ingredient` (
  `menu_item_id` INT NOT NULL,
  `ingredient_id` INT NOT NULL,
  `quantity` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`menu_item_id`,`ingredient_id`),
  FOREIGN KEY (`menu_item_id`) REFERENCES `menu_item`(`id`)
    ON DELETE CASCADE,
  FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient`(`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- Inventory (resources)
CREATE TABLE `inventory` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `ingredient_id` INT NOT NULL,
  `quantity` DECIMAL(12,2) NOT NULL,
  `unit_cost` DECIMAL(10,2),
  FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient`(`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- Orders
CREATE TABLE `orders` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `customer_id` INT NOT NULL,
  `tracking_number` VARCHAR(100) UNIQUE NOT NULL,
  `status` ENUM('pending','confirmed','preparing','ready','completed','cancelled')
    NOT NULL DEFAULT 'pending',
  `order_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `wait_time_minutes` INT DEFAULT NULL,
  `total_amount` DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (`customer_id`) REFERENCES `customer`(`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- Order items
CREATE TABLE `order_item` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `menu_item_id` INT NOT NULL,
  `quantity` INT NOT NULL,
  `item_price` DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`)
    ON DELETE CASCADE,
  FOREIGN KEY (`menu_item_id`) REFERENCES `menu_item`(`id`)
    ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Payments
CREATE TABLE `payment` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  `method` ENUM('card','paypal','cash','wallet') NOT NULL,
  `status` ENUM('pending','success','failure') NOT NULL DEFAULT 'pending',
  `transaction_id` VARCHAR(100),
  `payment_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- Feedback
CREATE TABLE `feedback` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `rating` INT CHECK (`rating` BETWEEN 1 AND 5),
  `message` TEXT,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`)
    ON DELETE CASCADE,
  FOREIGN KEY (`customer_id`) REFERENCES `customer`(`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- Staff users / roles
CREATE TABLE `staff_user` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) UNIQUE NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` ENUM('staff','admin','owner') NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB; 