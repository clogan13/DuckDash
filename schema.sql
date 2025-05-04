-- Duckdash Database Schema (MySQL)
-- Share this file with your group to ensure everyone has the same tables

-- Create the database
CREATE DATABASE IF NOT EXISTS `Duckdash`
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
USE `Duckdash`;

-- Customers (guests)
CREATE TABLE IF NOT EXISTS `customer` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(20),
  `email` VARCHAR(255),
  `address` VARCHAR(255),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Users (for authentication)
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Promotions
CREATE TABLE IF NOT EXISTS `promotion` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `code` VARCHAR(50) UNIQUE NOT NULL,
  `discount_amount` DECIMAL(10,2) DEFAULT NULL,
  `discount_percent` DECIMAL(5,2) DEFAULT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `usage_limit` INT DEFAULT NULL
) ENGINE=InnoDB;

-- Menu items
CREATE TABLE IF NOT EXISTS `menu_item` (
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
CREATE TABLE IF NOT EXISTS `ingredient` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `unit` VARCHAR(50)
) ENGINE=InnoDB;

-- Menu‐Item ⇄ Ingredient (many‐to‐many)
CREATE TABLE IF NOT EXISTS `menu_item_ingredient` (
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
CREATE TABLE IF NOT EXISTS `inventory` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `ingredient_id` INT NOT NULL,
  `quantity` DECIMAL(12,2) NOT NULL,
  `unit_cost` DECIMAL(10,2),
  FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient`(`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- Orders
CREATE TABLE IF NOT EXISTS `orders` (
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

-- Order status history
CREATE TABLE IF NOT EXISTS `order_status_history` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `status` ENUM('pending','confirmed','preparing','ready','completed','cancelled') NOT NULL,
  `changed_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `changed_by` INT,  -- Staff user ID who made the change
  `notes` TEXT,      -- Optional notes about the status change
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`)
    ON DELETE CASCADE,
  FOREIGN KEY (`changed_by`) REFERENCES `users`(`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB;

-- Order items
CREATE TABLE IF NOT EXISTS `order_item` (
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
CREATE TABLE IF NOT EXISTS `payment` (
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
CREATE TABLE IF NOT EXISTS `feedback` (
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
CREATE TABLE IF NOT EXISTS `staff_user` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) UNIQUE NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` ENUM('staff','admin','owner') NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB; 