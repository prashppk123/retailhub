"""
RetailHub - Database Setup Script
Reinitializes and migrates SQLite database schema with User Authentication.
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


def initialize_database(reset=False):
    print("=" * 60)
    print(" [Python] Initializing RetailHub SQLite Database")
    print("=" * 60)

    os.makedirs(DB_DIR, exist_ok=True)

    if not os.path.exists(SCHEMA_PATH):
        print(f"Error: Schema file not found at {SCHEMA_PATH}")
        sys.exit(1)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if migration is needed for customers table (password_hash)
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='customers'")
        table_exists = cursor.fetchone()[0] > 0

        if table_exists:
            cursor.execute("PRAGMA table_info(customers)")
            columns = [col[1] for col in cursor.fetchall()]
            if "password_hash" not in columns or reset:
                print("-> Migrating customers table to support authentication...")
                cursor.execute("DROP TABLE IF EXISTS order_items")
                cursor.execute("DROP TABLE IF EXISTS orders")
                cursor.execute("DROP TABLE IF EXISTS customers")

        # Read and apply schema
        print(f"-> Applying schema: {os.path.basename(SCHEMA_PATH)}...")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        print("   [OK] Schema tables, constraints, and views created.")

        # Read and apply seed data
        if os.path.exists(SEED_PATH):
            print(f"-> Loading seed data: {os.path.basename(SEED_PATH)}...")
            with open(SEED_PATH, "r", encoding="utf-8") as f:
                cursor.executescript(f.read())
            print("   [OK] Seed data inserted.")

        conn.commit()

        # Verification stats
        print("\n-> Database Statistics:")
        tables = ["categories", "products", "customers", "orders", "order_items"]
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   * Table '{table}': {count} records")

        conn.close()
        print("\n" + "=" * 60)
        print(f" [SUCCESS] Database ready at:\n {DB_PATH}")
        print("=" * 60)

    except sqlite3.Error as e:
        print(f" SQLite Error during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    initialize_database()
