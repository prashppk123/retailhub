-- ============================================================
-- RetailHub Analytical & Educational SQL Queries
-- Use these queries in Python, .NET, or any SQL client!
-- ============================================================

-- ------------------------------------------------------------
-- 1. BASIC FILTERING & SORTING
-- Find all active products with stock less than 10 units (low stock)
-- ------------------------------------------------------------
SELECT 
    product_id,
    sku,
    name,
    unit_price,
    stock_quantity
FROM products
WHERE is_active = 1 AND stock_quantity < 10
ORDER BY stock_quantity ASC;

-- ------------------------------------------------------------
-- 2. INNER JOIN & ALIASES
-- List all products with their category names
-- ------------------------------------------------------------
SELECT 
    p.product_id,
    p.sku,
    p.name AS product_name,
    c.name AS category_name,
    p.unit_price,
    p.stock_quantity
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
ORDER BY c.name, p.name;

-- ------------------------------------------------------------
-- 3. AGGREGATION & GROUP BY
-- Total sales revenue and units sold per product category
-- ------------------------------------------------------------
SELECT 
    c.name AS category,
    COUNT(DISTINCT p.product_id) AS total_products,
    COALESCE(SUM(oi.quantity), 0) AS units_sold,
    COALESCE(ROUND(SUM(oi.subtotal), 2), 0.0) AS total_revenue
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY c.category_id
ORDER BY total_revenue DESC;

-- ------------------------------------------------------------
-- 4. GROUP BY WITH HAVING
-- Customers who have spent more than $150 in total
-- ------------------------------------------------------------
SELECT 
    c.customer_id,
    c.full_name,
    c.email,
    c.city,
    COUNT(o.order_id) AS order_count,
    ROUND(SUM(o.total_amount), 2) AS total_spend
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'COMPLETED'
GROUP BY c.customer_id
HAVING total_spend > 150.00
ORDER BY total_spend DESC;

-- ------------------------------------------------------------
-- 5. SUBQUERY & CTE (Common Table Expression)
-- Calculate each product's contribution % to total store revenue
-- ------------------------------------------------------------
WITH RevenueData AS (
    SELECT 
        p.name AS product_name,
        COALESCE(SUM(oi.subtotal), 0.0) AS product_revenue
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id
),
TotalStoreRevenue AS (
    SELECT SUM(product_revenue) AS total_store FROM RevenueData
)
SELECT 
    r.product_name,
    ROUND(r.product_revenue, 2) AS revenue,
    ROUND((r.product_revenue / t.total_store) * 100, 2) AS revenue_percentage
FROM RevenueData r, TotalStoreRevenue t
ORDER BY revenue DESC;

-- ------------------------------------------------------------
-- 6. FULL ORDER DETAILS (MULTI-TABLE JOIN)
-- View order header, customer info, and purchased line items
-- ------------------------------------------------------------
SELECT 
    o.order_id,
    o.order_date,
    c.full_name AS customer_name,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price,
    oi.subtotal
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id DESC, oi.item_id ASC;
