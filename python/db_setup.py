"""
RetailHub - Database Setup Script
Demonstrates Python sqlite3 fundamentals:
 - Connecting to SQLite database
 - Executing multi-statement SQL scripts (executescript)
 - Error handling with try/except
 - Path resolution across directories
"""

import os
import sqlite3
import sys

# Directory Paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_DIR = os.path.join(PROJECT_ROOT, "database")
DB_PATH = os.path.join(DB_DIR, "retail.db")
SCHEMA_PATH = os.path.join(PROJECT_ROOT, "sql", "schema.sql")
SEED_PATH = os.path.join(PROJECT_ROOT, "sql", "seed.sql")


def initialize_database():
    print("=" * 60)
    print(" [Python] Initializing RetailHub SQLite Database")
    print("=" * 60)

    # Ensure database directory exists
    os.makedirs(DB_DIR, exist_ok=True)

    if not os.path.exists(SCHEMA_PATH):
        print(f"Error: Schema file not found at {SCHEMA_PATH}")
        sys.exit(1)

    try:
        # Connect to SQLite (creates file if not exists)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Read and apply schema
        print(f"-> Reading schema: {os.path.basename(SCHEMA_PATH)}...")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        print("   [OK] Schema tables, constraints, and views created.")

        # Read and apply seed data
        if os.path.exists(SEED_PATH):
            print(f"-> Reading seed data: {os.path.basename(SEED_PATH)}...")
            with open(SEED_PATH, "r", encoding="utf-8") as f:
                seed_sql = f.read()
            cursor.executescript(seed_sql)
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
