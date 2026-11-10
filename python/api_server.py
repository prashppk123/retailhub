"""
RetailHub - Lightweight REST API Microservice
Built entirely using Python's standard library (http.server and sqlite3).
Zero external pip packages needed!

Endpoints:
  GET  /api/health
  GET  /api/products
  GET  /api/customers
  GET  /api/orders
  GET  /api/analytics
  POST /api/orders
"""

import json
import os
import socket
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "database", "retail.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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

        # Serve Frontend UI at root
        if path == "" or path == "/":
            frontend_path = os.path.join(PROJECT_ROOT, "frontend", "index.html")
            if os.path.exists(frontend_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(frontend_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        if path in ("/api", "/api/health"):
            self._send_json(200, {
                "service": "RetailHub REST API",
                "status": "Online",
                "endpoints": [
                    "GET / (Frontend Dashboard)",
                    "GET /api/products",
                    "GET /api/customers",
                    "GET /api/orders",
                    "GET /api/analytics",
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
            cursor.execute("SELECT customer_id, full_name, email, city, registered_at FROM customers")
            data = [dict(row) for row in cursor.fetchall()]
            conn.close()
            self._send_json(200, {"count": len(data), "customers": data})
            return

        if path == "/api/orders":
            cursor.execute("""
                SELECT o.order_id, o.order_date, c.full_name AS customer, o.total_amount, o.status
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                ORDER BY o.order_id DESC
            """)
            data = [dict(row) for row in cursor.fetchall()]
            conn.close()
            self._send_json(200, {"count": len(data), "orders": data})
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

        if path == "/api/orders":
            content_length = int(self.headers.get("Content-Length", 0))
            body_raw = self.rfile.read(content_length).decode("utf-8")
            try:
                payload = json.loads(body_raw)
                customer_id = int(payload.get("customer_id"))
                product_id = int(payload.get("product_id"))
                quantity = int(payload.get("quantity", 1))

                conn = get_db()
                cursor = conn.cursor()

                # Verify stock
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

                # Transaction
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


def get_local_ip():
    """Retrieve machine's LAN IP address for network sharing."""
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


def run_server(port=8080):
    # Bind to 0.0.0.0 to allow access from local machine AND other devices on the network
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, RetailApiHandler)
    local_ip = get_local_ip()

    print("=" * 68)
    print(" [RetailHub Server] Online & Ready for Network Access!")
    print("=" * 68)
    print(f"  * This Computer:       http://localhost:{port}/")
    print(f"  * Other Devices (LAN): http://{local_ip}:{port}/")
    print("-" * 68)
    print("  To access from your mobile phone or another PC:")
    print(f"  1. Ensure both devices are on the same Wi-Fi / network.")
    print(f"  2. Open: http://{local_ip}:{port}/ in your browser.")
    print("=" * 68)
    print(" Press Ctrl+C to stop the server.")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    run_server()
