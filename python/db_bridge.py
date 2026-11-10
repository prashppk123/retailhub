"""
RetailHub - Python Database CLI Bridge
Accepts queries or commands from external programs (such as .NET) and outputs JSON.
Usage:
  python db_bridge.py query "<SQL SELECT>"
  python db_bridge.py execute "<SQL INSERT/UPDATE/DELETE>"
  python db_bridge.py order <customer_id> <product_id> <quantity>
"""

import json
import os
import sqlite3
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "database", "retail.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def handle_query(sql):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        conn.close()
        print(json.dumps({"success": True, "data": result}))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))


def handle_execute(sql):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        print(json.dumps({"success": True, "rows_affected": affected}))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))


def handle_place_order(customer_id, product_id, quantity):
    """
    Demonstrates SQL Transaction:
    1. Check stock
    2. Insert Order
    3. Insert Order Item
    4. Deduct Product Stock
    All inside an atomic transaction (commit or rollback).
    """
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check product stock and price
        cursor.execute(
            "SELECT product_id, name, unit_price, stock_quantity FROM products WHERE product_id = ?",
            (product_id,)
        )
        prod = cursor.fetchone()
        if not prod:
            print(json.dumps({"success": False, "error": f"Product ID {product_id} not found."}))
            return

        if prod["stock_quantity"] < quantity:
            print(json.dumps({
                "success": False, 
                "error": f"Insufficient stock. Available: {prod['stock_quantity']}, Requested: {quantity}."
            }))
            return

        unit_price = prod["unit_price"]
        total_amount = round(unit_price * quantity, 2)

        # Start transaction
        cursor.execute("BEGIN TRANSACTION")

        cursor.execute(
            "INSERT INTO orders (customer_id, total_amount, status) VALUES (?, ?, 'COMPLETED')",
            (customer_id, total_amount)
        )
        order_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
            (order_id, product_id, quantity, unit_price)
        )

        cursor.execute(
            "UPDATE products SET stock_quantity = stock_quantity - ? WHERE product_id = ?",
            (quantity, product_id)
        )

        conn.commit()
        conn.close()

        print(json.dumps({
            "success": True,
            "order_id": order_id,
            "product_name": prod["name"],
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total_amount
        }))
    except Exception as e:
        if conn:
            conn.rollback()
        print(json.dumps({"success": False, "error": str(e)}))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command specified."}))
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "query" and len(sys.argv) >= 3:
        handle_query(sys.argv[2])
    elif cmd == "execute" and len(sys.argv) >= 3:
        handle_execute(sys.argv[2])
    elif cmd == "order" and len(sys.argv) >= 5:
        handle_place_order(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    else:
        print(json.dumps({"error": "Invalid arguments."}))
