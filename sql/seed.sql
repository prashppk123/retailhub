-- ============================================================
-- Seed Data for RetailHub System
-- ============================================================

-- Categories
INSERT OR IGNORE INTO categories (category_id, name, description) VALUES
(1, 'Electronics', 'Gadgets, accessories, and computing hardware'),
(2, 'Home & Office', 'Desk accessories, stationery, and office furniture'),
(3, 'Apparel', 'Branded clothing and casual wear'),
(4, 'Beverages', 'Specialty coffee, tea, and mugs');

-- Products
INSERT OR IGNORE INTO products (product_id, category_id, sku, name, unit_price, stock_quantity, is_active) VALUES
(1, 1, 'ELEC-001', 'Wireless Noise-Cancelling Headphones', 149.99, 45, 1),
(2, 1, 'ELEC-002', 'Mechanical RGB Gaming Keyboard', 89.50, 60, 1),
(3, 1, 'ELEC-003', 'Ergonomic Vertical Mouse', 45.00, 8, 1),
(4, 1, 'ELEC-004', '4K Ultra-HD Webcam', 79.99, 5, 1),
(5, 2, 'OFF-001', 'Adjustable Dual Monitor Arm', 65.00, 25, 1),
(6, 2, 'OFF-002', 'Memory Foam Lumbar Support Cushion', 32.50, 40, 1),
(7, 2, 'OFF-003', 'Desk Cable Management Tray', 19.99, 12, 1),
(8, 3, 'APP-001', 'Developer Cotton Hoodie (Navy)', 49.99, 30, 1),
(9, 3, 'APP-002', 'Minimalist Tech Backpack', 69.00, 18, 1),
(10, 4, 'BEV-001', 'Single-Origin Ethiopian Coffee Beans (1lb)', 18.50, 80, 1),
(11, 4, 'BEV-002', 'Smart Temperature-Control Ceramic Mug', 55.00, 4, 1);

-- Customers
INSERT OR IGNORE INTO customers (customer_id, full_name, email, phone, city) VALUES
(1, 'Alice Johnson', 'alice.johnson@example.com', '+1-555-0101', 'Seattle'),
(2, 'Bob Smith', 'bob.smith@example.com', '+1-555-0102', 'Austin'),
(3, 'Carlos Mendez', 'carlos.m@example.com', '+1-555-0103', 'San Francisco'),
(4, 'Diana Patel', 'diana.patel@example.com', '+1-555-0104', 'New York'),
(5, 'Ethan Wright', 'ethan.w@example.com', '+1-555-0105', 'Chicago');

-- Orders
INSERT OR IGNORE INTO orders (order_id, customer_id, order_date, total_amount, status) VALUES
(1, 1, '2026-10-01 10:15:00', 239.49, 'COMPLETED'),
(2, 2, '2026-10-05 14:30:00', 89.50, 'COMPLETED'),
(3, 3, '2026-10-12 09:20:00', 166.49, 'COMPLETED'),
(4, 1, '2026-10-18 16:45:00', 55.00, 'COMPLETED'),
(5, 4, '2026-10-25 11:10:00', 214.99, 'COMPLETED'),
(6, 5, '2026-11-02 13:00:00', 119.98, 'COMPLETED');

-- Order Items
INSERT OR IGNORE INTO order_items (item_id, order_id, product_id, quantity, unit_price) VALUES
-- Order 1: Alice bought Headphones and Mechanical Keyboard
(1, 1, 1, 1, 149.99),
(2, 1, 2, 1, 89.50),
-- Order 2: Bob bought Keyboard
(3, 2, 2, 1, 89.50),
-- Order 3: Carlos bought Vertical Mouse, Monitor Arm, Coffee
(4, 3, 3, 1, 45.00),
(5, 3, 5, 1, 65.00),
(6, 3, 10, 3, 18.50),
-- Order 4: Alice bought Smart Mug
(7, 4, 11, 1, 55.00),
-- Order 5: Diana bought Headphones and Cable Tray
(8, 5, 1, 1, 149.99),
(9, 5, 7, 1, 19.99),
(10, 5, 6, 1, 32.50),
-- Order 6: Ethan bought Hoodie and Backpack
(11, 6, 8, 1, 49.99),
(12, 6, 9, 1, 69.00);
