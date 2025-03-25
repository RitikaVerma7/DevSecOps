CREATE DATABASE IF NOT EXISTS scu_food_delivery;
USE scu_food_delivery;  -- ✅ Ensure the database is selected before creating tables

CREATE USER IF NOT EXISTS 'scu_food'@'%' IDENTIFIED BY 'Odie@2014';
GRANT ALL PRIVILEGES ON scu_food_delivery.* TO 'scu_food'@'%';
FLUSH PRIVILEGES;

# Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    scu_email VARCHAR(255) NOT NULL UNIQUE,
    scu_id VARCHAR(255) NOT NULL UNIQUE
);


INSERT INTO users (name, scu_email, scu_id) VALUES ('Admin User', 'admin@scu.edu', '1234567890');

#menu_items Table

CREATE TABLE menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,  -- Breakfast, Lunch, Dinner, Drinks
    price DECIMAL(5, 2) NOT NULL
);

INSERT INTO menu_items (name, category, price) VALUES
('Cereal', 'Breakfast', 5.00),
('Pancakes', 'Breakfast', 8.00),
('Waffles', 'Breakfast', 7.50),
('Oatmeal', 'Breakfast', 6.50),
('Scrambled Eggs', 'Breakfast', 6.00),
('Avocado Toast', 'Breakfast', 9.00),
('Burrito Bowl', 'Lunch', 12.50),
('Sushi', 'Lunch', 15.00),
('Veggie Pizza', 'Lunch', 4.00),
('Greek Tuna Salad', 'Lunch', 14.00),
('Chicken Biryani', 'Lunch', 16.50),
('Beef Sliders', 'Lunch', 13.00),
('Crispy Buffalo Chicken Caesar Wrap', 'Dinner', 12.50),
('Hanoi Chilled Noodles', 'Dinner', 14.00),
('BBQ Chicken Pizza', 'Dinner', 6.00),
('Fried Mushroom Sandwich', 'Dinner', 13.50),
('Broccoli Crunch Salad', 'Dinner', 11.50),
('Water', 'Drinks', 2.00),
('Soda', 'Drinks', 2.50),
('Coffee', 'Drinks', 4.00),
('Matcha Latte', 'Drinks', 5.50),
('Smoothie', 'Drinks', 6.00);


#orders Table

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(255) NOT NULL,
    total_price DECIMAL(7, 2) NOT NULL,
    estimated_delivery_time INT,
    order_id VARCHAR(255) UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

#order_items Table

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);

Select * from users