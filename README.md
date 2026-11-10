# 🛍️ RetailHub: Sales, Inventory & Analytics System
> A complete full-stack learning project uniting **SQL**, **.NET (C#)**, and **Python**.

---

## 🎯 Architecture & Purpose

This project demonstrates how real-world enterprise architectures often combine specialized technologies:

```
                  ┌────────────────────────────────────────┐
                  │          SQLite Database               │
                  │        (retail.db + SQL Schema)        │
                  └───────────────▲────────────────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         │                                                 │
┌────────┴────────────────────────┐       ┌────────────────┴────────────────┐
│         .NET / C# App           │       │         Python Engine           │
│   (Business Logic & Inventory)  │       │     (Analytics, BI & REST API)  │
├─────────────────────────────────┤       ├─────────────────────────────────┤
│ • Strong-Typed Domain Models    │       │ • Analytical Reporting & BI     │
│ • Inventory & Stock Checking    │       │ • CSV & Markdown Report Export  │
│ • Transactional Order Placement │       │ • Lightweight REST HTTP API     │
│ • Interactive CLI Interface     │       │ • Zero external dependencies    │
└─────────────────────────────────┘       └─────────────────────────────────┘
```

---

## 📂 Project Directory Structure

```text
retail_analytics_hub/
│
├── sql/                          # 🗄️ SQL Database Layer
│   ├── schema.sql                # Table definitions, constraints, indexes, views
│   ├── seed.sql                  # Initial catalog, customer, and order data
│   └── queries.sql               # Educational analytical queries (JOINs, GROUP BY, CTEs)
│
├── dotnet/                       # 🔷 .NET / C# Application Layer
│   ├── Models/
│   │   ├── Product.cs            # Product entity model (OOP properties, formatting)
│   │   ├── Customer.cs           # Customer entity model
│   │   └── Order.cs              # Order & transaction model
│   ├── Services/
│   │   └── DatabaseService.cs    # Data access service (Queries, transactions, IPC bridge)
│   ├── Program.cs                # Interactive console app & menu
│   ├── RetailApp.csproj          # Modern .NET 8 SDK project definition
│   └── build.bat                 # One-click build script using csc compiler
│
├── python/                       # 🐍 Python Analytics & Microservice Layer
│   ├── db_setup.py               # Database builder (runs schema.sql & seed.sql)
│   ├── analytics.py              # Business intelligence engine (metrics, alerts, exports)
│   ├── api_server.py             # Lightweight HTTP REST API server
│   └── db_bridge.py              # CLI query bridge for C# integration
│
├── database/                     # Generated SQLite database file (retail.db)
├── reports/                      # Generated analytical exports (CSV & Markdown)
├── run.bat                       # Interactive Windows launcher menu
├── run.ps1                       # Interactive PowerShell launcher
└── README.md                     # Complete project documentation
```

---

## 💡 Concepts Demonstrated

### 1. SQL (Structured Query Language)
- **Data Definition Language (DDL)**: `CREATE TABLE`, `CREATE INDEX`, `CREATE VIEW`.
- **Integrity Constraints**: `PRIMARY KEY AUTOINCREMENT`, `FOREIGN KEY ... ON DELETE CASCADE`, `CHECK`, `UNIQUE`, `NOT NULL`, `DEFAULT`.
- **Aggregations & Grouping**: `COUNT()`, `SUM()`, `AVG()`, `GROUP BY`, and `HAVING`.
- **Joins**: `INNER JOIN`, `LEFT JOIN` linking products, categories, orders, customers, and order items.
- **Transactions**: `BEGIN TRANSACTION`, `COMMIT`, `ROLLBACK` ensuring stock deduction and order placement are atomic.
- **Computed Columns & CTEs**: Generated subtotal columns and Common Table Expressions for percentage calculations.

### 2. .NET / C# Basics
- **Object-Oriented Programming (OOP)**:
  - Class definitions, private/public encapsulation.
  - Auto-implemented properties (`{ get; set; }`).
  - Overloaded constructors.
  - Polymorphism (`override ToString()`).
- **Collections & Generics**: `List<Product>`, `List<Customer>`, `Dictionary<string, object>`.
- **Data Access & Business Logic**:
  - Input parsing, data validation, and error checking.
  - Inventory validation before confirming purchases.
  - Modern project structure (`.csproj`) for .NET 8 / Visual Studio + built-in fallback compiler compatibility.

### 3. Python Basics
- **Database Connectivity**: Built-in `sqlite3` module with `sqlite3.Row` for dictionary-like column access.
- **Business Intelligence**: Calculating key retail metrics (Revenue, Average Order Value, Category share, Low-stock alerts).
- **File I/O & Reporting**: Exporting reports to both CSV (`csv.writer`) and structured Markdown.
- **Microservices & Networking**: Creating a functional HTTP REST API using Python's standard library `http.server` with zero external pip dependencies.

---

## 🚀 Quick Start Guide

### Option A: The All-in-One Launcher (Recommended)
Double-click `run.bat` (or run `./run.ps1` in PowerShell) in the project root:
```powershell
.\run.ps1
```
This presents an interactive menu to run any component with a single keystroke.

---

### Option B: Running Individual Components Manually

#### Step 1: Initialize the SQL Database
```powershell
python python/db_setup.py
```
*Creates `database/retail.db` and loads schema & seed data.*

#### Step 2: Run the .NET / C# Application
```powershell
# Run the pre-compiled executable directly:
.\dotnet\RetailApp.exe

# Or recompile it anytime with:
.\dotnet\build.bat

# If you have .NET 8 SDK installed, you can also run:
dotnet run --project dotnet/RetailApp.csproj
```

#### Step 3: Run the Python Business Intelligence & Analytics Report
```powershell
python python/analytics.py
```
*Outputs an executive summary in your terminal and generates `reports/analytics_report.md` and `reports/product_sales_summary.csv`.*

#### Step 4: Start the Python REST API Server
```powershell
python python/api_server.py
```
*Starts a local HTTP server at `http://127.0.0.1:8080/`.*
Try opening these URLs in your browser or with `curl`:
- `http://127.0.0.1:8080/api/products` (Catalog listing)
- `http://127.0.0.1:8080/api/orders` (Order list)
- `http://127.0.0.1:8080/api/analytics` (Summary KPIs & low-stock alerts)
- `http://127.0.0.1:8080/api/customers` (Customer list)

---

## 🧪 Testing the Transactional Flow

Try this test to see how .NET, SQL, and Python interact in real-time:
1. Run `python python/analytics.py` and observe the stock for product **`ELEC-003` (Ergonomic Vertical Mouse)**.
2. Launch `dotnet/RetailApp.exe`, choose **Option 3 (Place Order)**, and purchase 2 units of Product ID `3`.
3. Notice that the .NET app atomically inserts the order, records the line items, and deducts the inventory in SQL.
4. Run `python python/analytics.py` again — notice the revenue increases and the stock quantity has updated!
