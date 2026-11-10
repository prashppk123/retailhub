-- ============================================================
-- Seed Data for RetailHub Indian E-Commerce Store
-- Currency: Indian Rupee (INR - ₹)
-- Default Password for Demo Users: password123
-- ============================================================

-- Categories
INSERT OR IGNORE INTO categories (category_id, name, description) VALUES
(1, 'Smartphones', 'Flagship and premium 5G smartphones'),
(2, 'Laptops & Computers', 'High-performance laptops for creators and gamers'),
(3, 'Furniture', 'Ergonomic office and modern living space furniture'),
(4, 'Audio & Wearables', 'Noise-cancelling headphones and smart fitness watches');

-- Products with Images and Indian Rupee (INR) Pricing
INSERT OR IGNORE INTO products (product_id, category_id, sku, name, image_url, unit_price, stock_quantity, is_active) VALUES
-- Smartphones
(1, 1, 'PHONE-001', 'Apple iPhone 15 Pro (128GB, Natural Titanium)', 
 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&auto=format&fit=crop&q=80', 
 124999.00, 35, 1),

(2, 1, 'PHONE-002', 'Samsung Galaxy S24 Ultra (256GB, Titanium Black)', 
 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600&auto=format&fit=crop&q=80', 
 119999.00, 42, 1),

(3, 1, 'PHONE-003', 'OnePlus 12 5G (16GB RAM, Emerald Green)', 
 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop&q=80', 
 64999.00, 20, 1),

-- Laptops & Computers
(4, 2, 'LAP-001', 'Apple MacBook Pro M3 (14-inch, Space Black)', 
 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=80', 
 169900.00, 18, 1),

(5, 2, 'LAP-002', 'Dell XPS 15 OLED (Intel Core i9, 32GB RAM)', 
 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=600&auto=format&fit=crop&q=80', 
 184990.00, 10, 1),

(6, 2, 'LAP-003', 'ASUS ROG Strix G16 Gaming Laptop (RTX 4070)', 
 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=600&auto=format&fit=crop&q=80', 
 139990.00, 15, 1),

-- Furniture
(7, 3, 'FURN-001', 'Ergonomic High-Back Executive Mesh Chair', 
 'https://images.unsplash.com/photo-1580481077167-27b613143c4a?w=600&auto=format&fit=crop&q=80', 
 14499.00, 25, 1),

(8, 3, 'FURN-002', 'Motorized Dual-Motor Height Adjustable Standing Desk', 
 'https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?w=600&auto=format&fit=crop&q=80', 
 28990.00, 12, 1),

(9, 3, 'FURN-003', 'Modern Solid Oak Wood Bookshelf & Display Rack', 
 'https://images.unsplash.com/photo-1594980596870-8aa52a78d8cd?w=600&auto=format&fit=crop&q=80', 
 12999.00, 8, 1),

-- Audio & Wearables
(10, 4, 'AUD-001', 'Sony WH-1000XM5 Wireless Noise Cancelling Headphones', 
 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80', 
 26990.00, 50, 1),

(11, 4, 'AUD-002', 'Apple Watch Series 9 GPS + Cellular (Midnight)', 
 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80', 
 41900.00, 22, 1);

-- Registered Customers
INSERT OR IGNORE INTO customers (customer_id, full_name, email, password_hash, phone, city, role) VALUES
(1, 'Rahul Sharma', 'rahul.sharma@example.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', '+91-98765-43210', 'Bangalore', 'CUSTOMER'),
(2, 'Priya Patel', 'priya.patel@example.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', '+91-98765-43211', 'Mumbai', 'CUSTOMER'),
(3, 'Amit Verma', 'amit.verma@example.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', '+91-98765-43212', 'Delhi', 'CUSTOMER'),
(4, 'Sneha Reddy', 'sneha.reddy@example.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', '+91-98765-43213', 'Hyderabad', 'CUSTOMER'),
(5, 'Vikram Singh', 'vikram.singh@example.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', '+91-98765-43214', 'Pune', 'CUSTOMER'),
(6, 'Store Admin', 'admin@retailhub.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', '+91-98000-00000', 'HQ', 'ADMIN');

-- Sample Initial Orders
INSERT OR IGNORE INTO orders (order_id, customer_id, order_date, total_amount, status) VALUES
(1, 1, '2026-11-01 11:30:00', 124999.00, 'COMPLETED'),
(2, 2, '2026-11-04 14:15:00', 41489.00, 'COMPLETED');

-- Order Items
INSERT OR IGNORE INTO order_items (item_id, order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1, 124999.00),
(2, 2, 7, 1, 14499.00),
(3, 2, 10, 1, 26990.00);
