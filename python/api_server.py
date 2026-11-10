"""
RetailHub - Lightweight REST API Microservice
Includes Customer Registration, Authentication, and Order Management.
Zero external pip packages needed!

Endpoints:
  GET  / (Serves Frontend Storefront)
  GET  /api/health
  GET  /api/products
  GET  /api/customers
  GET  /api/orders
  GET  /api/user/orders?customer_id=1
  GET  /api/analytics
  POST /api/auth/register
  POST /api/auth/login
  POST /api/orders
"""

import hashlib
import json
import os
import socket
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "database", "retail.db")


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


class RetailApiHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        query = parse_qs(parsed.query)

        # Serve Frontend UI at root
        if path == "" or path == "/":
            frontend_path = os.path.join(PROJECT_ROOT, "frontend", "index.html")
            if not os.path.exists(frontend_path):
                frontend_path = os.path.join(PROJECT_ROOT, "index.html")

            if os.path.exists(frontend_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(frontend_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        if path in ("/api", "/api/health"):
            self._send_json(200, {
                "service": "RetailHub REST API with Registration",
                "status": "Online",
                "endpoints": [
                    "GET / (Frontend Dashboard)",
                    "GET /api/products",
                    "GET /api/customers",
                    "GET /api/orders",
                    "GET /api/user/orders?customer_id=1",
                    "GET /api/analytics",
                    "POST /api/auth/register",
                    "POST /api/auth/login",
                    "POST /api/orders"
                ]
            })
            return

        conn = get_db()
        cursor = conn.cursor()

        if path == "/api/products":
            cursor.execute("""
                SELECT p.product_id, p.sku, p.name, c.name AS category, p.unit_price, p.stock_quantity
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                WHERE p.is_active = 1
                ORDER BY p.product_id
            """)
            data = [dict(row) for row in cursor.fetchall()]
            conn.close()
            self._send_json(200, {"count": len(data), "products": data})
            return

        if path == "/api/customers":
            cursor.execute("SELECT customer_id, full_name, email, city, role, registered_at FROM customers ORDER BY customer_id")
            data = [dict(row) for row in cursor.fetchall()]
            conn.close()
            self._send_json(200, {"count": len(data), "customers": data})
            return

        if path == "/api/orders":
            cursor.execute("""
                SELECT o.order_id, o.customer_id, o.order_date, c.full_name AS customer, o.total_amount, o.status
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                ORDER BY o.order_id DESC
            """)
            data = [dict(row) for row in cursor.fetchall()]
            conn.close()
            self._send_json(200, {"count": len(data), "orders": data})
            return

        if path == "/api/user/orders":
            cust_id = query.get("customer_id", [None])[0]
            if not cust_id:
                conn.close()
                self._send_json(400, {"error": "Missing customer_id query parameter."})
                return

            cursor.execute("""
                SELECT o.order_id, o.order_date, o.total_amount, o.status,
                       GROUP_CONCAT(p.name || ' (x' || oi.quantity || ')', ', ') AS items_summary
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                JOIN products p ON oi.product_id = p.product_id
                WHERE o.customer_id = ?
                GROUP BY o.order_id
                ORDER BY o.order_id DESC
            """, (cust_id,))
            orders = [dict(row) for row in cursor.fetchall()]
            conn.close()
            self._send_json(200, {"count": len(orders), "orders": orders})
            return

        if path == "/api/analytics":
            cursor.execute("""
                SELECT 
                    COUNT(*) AS total_orders,
                    ROUND(SUM(total_amount), 2) AS total_revenue,
                    ROUND(AVG(total_amount), 2) AS avg_order_value
                FROM orders WHERE status = 'COMPLETED'
            """)
            summary = dict(cursor.fetchone())

            cursor.execute("""
                SELECT sku, name, stock_quantity 
                FROM products 
                WHERE is_active = 1 AND stock_quantity <= 10
            """)
            low_stock = [dict(row) for row in cursor.fetchall()]
            conn.close()

            self._send_json(200, {
                "summary": summary,
                "low_stock_alerts": low_stock
            })
            return

        conn.close()
        self._send_json(404, {"error": f"Endpoint '{self.path}' not found."})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        content_length = int(self.headers.get("Content-Length", 0))
        body_raw = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            payload = json.loads(body_raw)
        except Exception:
            payload = {}

        # 1. Customer Registration
        if path == "/api/auth/register":
            full_name = payload.get("full_name", "").strip()
            email = payload.get("email", "").strip().lower()
            password = payload.get("password", "")
            city = payload.get("city", "Online").strip()
            phone = payload.get("phone", "").strip()

            if not full_name or not email or not password:
                self._send_json(400, {"success": False, "error": "Full name, email, and password are required."})
                return

            if len(password) < 4:
                self._send_json(400, {"success": False, "error": "Password must be at least 4 characters."})
                return

            try:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT customer_id FROM customers WHERE email = ?", (email,))
                if cursor.fetchone():
                    conn.close()
                    self._send_json(409, {"success": False, "error": f"Email '{email}' is already registered."})
                    return

                pwd_hash = hash_password(password)
                cursor.execute(
                    "INSERT INTO customers (full_name, email, password_hash, phone, city, role) VALUES (?, ?, ?, ?, ?, 'CUSTOMER')",
                    (full_name, email, pwd_hash, phone, city)
                )
                conn.commit()
                new_id = cursor.lastrowid
                conn.close()

                self._send_json(201, {
                    "success": True,
                    "message": "Registration successful!",
                    "user": {
                        "customer_id": new_id,
                        "full_name": full_name,
                        "email": email,
                        "city": city,
                        "role": "CUSTOMER"
                    }
                })
            except Exception as e:
                self._send_json(500, {"success": False, "error": str(e)})
            return

        # 2. Customer Login
        if path == "/api/auth/login":
            email = payload.get("email", "").strip().lower()
            password = payload.get("password", "")

            if not email or not password:
                self._send_json(400, {"success": False, "error": "Email and password are required."})
                return

            try:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT customer_id, full_name, email, password_hash, city, role FROM customers WHERE email = ?",
                    (email,)
                )
                user = cursor.fetchone()
                conn.close()

                if not user or user["password_hash"] != hash_password(password):
                    self._send_json(401, {"success": False, "error": "Invalid email or password."})
                    return

                self._send_json(200, {
                    "success": True,
                    "message": f"Welcome back, {user['full_name']}!",
                    "user": {
                        "customer_id": user["customer_id"],
                        "full_name": user["full_name"],
                        "email": user["email"],
                        "city": user["city"],
                        "role": user["role"]
                    }
                })
            except Exception as e:
                self._send_json(500, {"success": False, "error": str(e)})
            return

        # 3. Create Sales Order
        if path == "/api/orders":
            try:
                customer_id = int(payload.get("customer_id"))
                product_id = int(payload.get("product_id"))
                quantity = int(payload.get("quantity", 1))

                conn = get_db()
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT product_id, name, unit_price, stock_quantity FROM products WHERE product_id = ?",
                    (product_id,)
                )
                prod = cursor.fetchone()
                if not prod:
                    conn.close()
                    self._send_json(404, {"error": f"Product {product_id} not found."})
                    return

                if prod["stock_quantity"] < quantity:
                    conn.close()
                    self._send_json(400, {
                        "error": f"Insufficient stock. Available: {prod['stock_quantity']}"
                    })
                    return

                total_amount = round(prod["unit_price"] * quantity, 2)

                cursor.execute("BEGIN TRANSACTION")
                cursor.execute(
                    "INSERT INTO orders (customer_id, total_amount, status) VALUES (?, ?, 'COMPLETED')",
                    (customer_id, total_amount)
                )
                order_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                    (order_id, product_id, quantity, prod["unit_price"])
                )
                cursor.execute(
                    "UPDATE products SET stock_quantity = stock_quantity - ? WHERE product_id = ?",
                    (quantity, product_id)
                )
                conn.commit()
                conn.close()

                self._send_json(201, {
                    "message": "Order created successfully",
                    "order_id": order_id,
                    "product": prod["name"],
                    "quantity": quantity,
                    "total_amount": total_amount
                })
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        self._send_json(404, {"error": f"Endpoint '{self.path}' not found."})


def run_server(port=8080):
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, RetailApiHandler)
    local_ip = get_local_ip()

    print("=" * 68)
    print(" [RetailHub Server] Online & Ready for Network Access!")
    print("=" * 68)
    print(f"  * This Computer:       http://localhost:{port}/")
    print(f"  * Other Devices (LAN): http://{local_ip}:{port}/")
    print("-" * 68)
    print(" Press Ctrl+C to stop the server.")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    run_server()
