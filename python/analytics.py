"""
RetailHub - Python Analytics & Business Intelligence Engine
Demonstrates:
 - Python SQLite querying with sqlite3.Row
 - Data aggregation, formatting, and analysis
 - File handling (Writing Markdown reports and CSV data exports)
 - Clean console dashboards
"""

import csv
import os
import sqlite3
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "database", "retail.db")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables column access by name
    return conn


def print_table(headers, rows, col_widths=None):
    """Helper function to print formatted ASCII tables."""
    if not col_widths:
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val)))

    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    sep_line = "-+-".join("-" * w for w in col_widths)

    print(header_line)
    print(sep_line)
    for row in rows:
        print(" | ".join(str(val).ljust(w) for val, w in zip(row, col_widths)))
    print()


def run_analytics():
    print("=" * 70)
    print("        RETAILHUB BUSINESS INTELLIGENCE & ANALYTICS REPORT        ")
    print("=" * 70)
    print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    os.makedirs(REPORTS_DIR, exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. High-Level Metrics
    cursor.execute("""
        SELECT 
            (SELECT COUNT(*) FROM products WHERE is_active = 1) AS total_products,
            (SELECT COUNT(*) FROM customers) AS total_customers,
            (SELECT COUNT(*) FROM orders WHERE status = 'COMPLETED') AS total_orders,
            (SELECT ROUND(SUM(total_amount), 2) FROM orders WHERE status = 'COMPLETED') AS total_revenue,
            (SELECT ROUND(AVG(total_amount), 2) FROM orders WHERE status = 'COMPLETED') AS avg_order_value
    """)
    stats = cursor.fetchone()

    print("--- 1. EXECUTIVE SUMMARY ---")
    print(f" Active Products in Catalog: {stats['total_products']}")
    print(f" Registered Customers:       {stats['total_customers']}")
    print(f" Completed Orders:           {stats['total_orders']}")
    print(f" Total Revenue:              ${stats['total_revenue']:,.2f}")
    print(f" Average Order Value (AOV):  ${stats['avg_order_value']:,.2f}\n")

    # 2. Sales by Category
    print("--- 2. PERFORMANCE BY CATEGORY ---")
    cursor.execute("""
        SELECT 
            c.name AS category,
            COUNT(DISTINCT p.product_id) AS products_count,
            COALESCE(SUM(oi.quantity), 0) AS units_sold,
            COALESCE(ROUND(SUM(oi.subtotal), 2), 0.0) AS revenue
        FROM categories c
        LEFT JOIN products p ON c.category_id = p.category_id
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY c.category_id
        ORDER BY revenue DESC
    """)
    cat_rows = cursor.fetchall()
    cat_headers = ["Category", "Products", "Units Sold", "Revenue ($)"]
    cat_data = [
        [row["category"], row["products_count"], row["units_sold"], f"${row['revenue']:,.2f}"]
        for row in cat_rows
    ]
    print_table(cat_headers, cat_data)

    # 3. Top-Selling Products
    print("--- 3. TOP-SELLING PRODUCTS ---")
    cursor.execute("""
        SELECT 
            p.sku,
            p.name,
            c.name AS category,
            COALESCE(SUM(oi.quantity), 0) AS total_sold,
            COALESCE(ROUND(SUM(oi.subtotal), 2), 0.0) AS revenue
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id
        ORDER BY revenue DESC
        LIMIT 5
    """)
    top_products = cursor.fetchall()
    top_headers = ["SKU", "Product Name", "Category", "Sold", "Total Revenue"]
    top_data = [
        [r["sku"], r["name"][:28], r["category"], r["total_sold"], f"${r['revenue']:,.2f}"]
        for r in top_products
    ]
    print_table(top_headers, top_data)

    # 4. Low-Stock Alerts (Inventory <= 10)
    print("--- 4. LOW-STOCK INVENTORY ALERTS (Action Needed) ---")
    cursor.execute("""
        SELECT sku, name, unit_price, stock_quantity
        FROM products
        WHERE is_active = 1 AND stock_quantity <= 10
        ORDER BY stock_quantity ASC
    """)
    low_stock = cursor.fetchall()
    alert_headers = ["SKU", "Product Name", "Price", "Stock Remaining"]
    alert_data = [
        [r["sku"], r["name"][:30], f"${r['unit_price']:,.2f}", f"{r['stock_quantity']} units [LOW]"]
        for r in low_stock
    ]
    print_table(alert_headers, alert_data)

    # 5. Top Customer Lifetime Value
    print("--- 5. TOP CUSTOMERS BY SPEND ---")
    cursor.execute("""
        SELECT 
            c.full_name,
            c.email,
            c.city,
            COUNT(o.order_id) AS total_orders,
            ROUND(SUM(o.total_amount), 2) AS total_spent
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.status = 'COMPLETED'
        GROUP BY c.customer_id
        ORDER BY total_spent DESC
    """)
    top_customers = cursor.fetchall()
    cust_headers = ["Customer Name", "Email", "City", "Orders", "Total Spent"]
    cust_data = [
        [c["full_name"], c["email"], c["city"], c["total_orders"], f"${c['total_spent']:,.2f}"]
        for c in top_customers
    ]
    print_table(cust_headers, cust_data)

    # Export to CSV
    csv_file = os.path.join(REPORTS_DIR, "product_sales_summary.csv")
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["SKU", "Product Name", "Category", "Units Sold", "Revenue USD"])
        for r in top_products:
            writer.writerow([r["sku"], r["name"], r["category"], r["total_sold"], r["revenue"]])
    print(f"[OK] Exported CSV report to: {csv_file}")

    # Export to Markdown
    md_file = os.path.join(REPORTS_DIR, "analytics_report.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# RetailHub Sales & Inventory Report\n\n")
        f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("## 1. Key Metrics\n\n")
        f.write(f"- **Total Revenue**: ${stats['total_revenue']:,.2f}\n")
        f.write(f"- **Completed Orders**: {stats['total_orders']}\n")
        f.write(f"- **Average Order Value**: ${stats['avg_order_value']:,.2f}\n")
        f.write(f"- **Active Products**: {stats['total_products']}\n\n")
        f.write("## 2. Low-Stock Alerts\n\n")
        f.write("| SKU | Product Name | Stock Remaining |\n|---|---|---|\n")
        for r in low_stock:
            f.write(f"| {r['sku']} | {r['name']} | **{r['stock_quantity']}** |\n")
    print(f"[OK] Exported Markdown report to: {md_file}")

    conn.close()
    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_analytics()
