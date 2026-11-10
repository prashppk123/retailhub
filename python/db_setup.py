"""
RetailHub - Database Setup & Migration Script
Builds SQLite database with Indian Rupee (INR) catalog and product images.
"""

import os
import sqlite3
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_DIR = os.path.join(PROJECT_ROOT, "database")
DB_PATH = os.path.join(DB_DIR, "retail.db")
SCHEMA_PATH = os.path.join(PROJECT_ROOT, "sql", "schema.sql")
SEED_PATH = os.path.join(PROJECT_ROOT, "sql", "seed.sql")


def initialize_database():
    print("=" * 65)
    print(" [Python] Initializing RetailHub Database (INR / Product Images)")
    print("=" * 65)

    os.makedirs(DB_DIR, exist_ok=True)

    if not os.path.exists(SCHEMA_PATH):
        print(f"Error: Schema file not found at {SCHEMA_PATH}")
        sys.exit(1)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Recreate tables to ensure schema matches new image_url column
        cursor.execute("DROP VIEW IF EXISTS v_product_sales_summary")
        cursor.execute("DROP TABLE IF EXISTS order_items")
        cursor.execute("DROP TABLE IF EXISTS orders")
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.execute("DROP TABLE IF EXISTS customers")
        cursor.execute("DROP TABLE IF EXISTS categories")

        # Read and apply schema
        print(f"-> Applying schema: {os.path.basename(SCHEMA_PATH)}...")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        print("   [OK] Tables created with image_url and foreign keys.")

        # Read and apply seed data
        if os.path.exists(SEED_PATH):
            print(f"-> Loading seed data: {os.path.basename(SEED_PATH)}...")
            with open(SEED_PATH, "r", encoding="utf-8") as f:
                cursor.executescript(f.read())
            print("   [OK] Seed products (Smartphones, Laptops, Furniture) inserted.")

        conn.commit()

        # Verification stats
        print("\n-> Backend Database Verification:")
        tables = ["categories", "products", "customers", "orders", "order_items"]
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   * Table '{table}': {count} records")

        conn.close()
        print("\n" + "=" * 65)
        print(f" [SUCCESS] Database ready at:\n {DB_PATH}")
        print("=" * 65)

    except sqlite3.Error as e:
        print(f" SQLite Error during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    initialize_database()
