using System;
using System.Collections.Generic;
using RetailHub.Models;
using RetailHub.Services;

namespace RetailHub
{
    class Program
    {
        static DatabaseService _db = new DatabaseService();

        static void Main(string[] args)
        {
            try
            {
                Console.Title = "RetailHub - Sales, Inventory & SQL Manager (.NET / C#)";
            }
            catch {}

            if (args.Length > 0 && args[0].ToLower() == "--demo")
            {
                RunDemoMode();
                return;
            }

            bool exit = false;
            while (!exit)
            {
                PrintMenu();
                Console.Write("Enter your choice (0-6): ");
                string choice = Console.ReadLine();

                Console.WriteLine();
                switch (choice)
                {
                    case "1":
                        ListProducts();
                        break;
                    case "2":
                        AddNewProduct();
                        break;
                    case "3":
                        PlaceCustomerOrder();
                        break;
                    case "4":
                        RestockInventory();
                        break;
                    case "5":
                        ViewOrderHistory();
                        break;
                    case "6":
                        RegisterNewCustomer();
                        break;
                    case "7":
                        RunCustomSql();
                        break;
                    case "0":
                        exit = true;
                        Console.WriteLine("Exiting RetailHub .NET Manager. Goodbye!");
                        break;
                    default:
                        Console.WriteLine("Invalid option. Please enter a number between 0 and 7.");
                        break;
                }

                if (!exit)
                {
                    Console.WriteLine("\nPress Enter to continue...");
                    Console.ReadLine();
                }
            }
        }

        static void PrintMenu()
        {
            try { Console.Clear(); } catch {}
            Console.WriteLine("==================================================================");
            Console.WriteLine("           RETAILHUB INVENTORY & ORDER MANAGEMENT (.NET)         ");
            Console.WriteLine("==================================================================");
            Console.WriteLine("  1. View Product Catalog & Inventory Levels");
            Console.WriteLine("  2. Add New Product to Catalog");
            Console.WriteLine("  3. Place New Customer Order (SQL Transaction)");
            Console.WriteLine("  4. Restock Existing Product");
            Console.WriteLine("  5. View Customer Orders & Revenue");
            Console.WriteLine("  6. Register New Customer / User Account");
            Console.WriteLine("  7. Run Custom SQL Query");
            Console.WriteLine("  0. Exit");
            Console.WriteLine("==================================================================");
        }

        static void ListProducts()
        {
            Console.WriteLine("--- Current Product Catalog ---");
            Console.WriteLine(new string('-', 85));
            Console.WriteLine(string.Format("{0,2} {1,-9} | {2,-32} | {3,-13} | {4,9} | {5,5}",
                "ID", "SKU", "Product Name", "Category", "Price", "Stock"));
            Console.WriteLine(new string('-', 85));

            var products = _db.GetProducts();
            foreach (var p in products)
            {
                string alert = p.StockQuantity <= 5 ? " [CRITICAL]" : (p.StockQuantity <= 10 ? " [LOW]" : "");
                Console.WriteLine(string.Format("{0}{1}", p, alert));
            }
            Console.WriteLine(new string('-', 85));
            Console.WriteLine(string.Format("Total products: {0}", products.Count));
        }

        static void AddNewProduct()
        {
            Console.WriteLine("--- Add New Product ---");
            Console.Write("Enter SKU (e.g., ELEC-005): ");
            string sku = Console.ReadLine();
            if (sku != null) sku = sku.Trim();

            Console.Write("Enter Product Name: ");
            string name = Console.ReadLine();
            if (name != null) name = name.Trim();

            Console.WriteLine("\nSelect Category ID:");
            Console.WriteLine("  1 = Electronics | 2 = Home & Office | 3 = Apparel | 4 = Beverages");
            Console.Write("Enter Category ID (1-4): ");
            int categoryId;
            if (!int.TryParse(Console.ReadLine(), out categoryId) || categoryId < 1 || categoryId > 4)
            {
                Console.WriteLine("Invalid category ID.");
                return;
            }

            Console.Write("Enter Unit Price ($): ");
            decimal price;
            if (!decimal.TryParse(Console.ReadLine(), out price) || price < 0)
            {
                Console.WriteLine("Invalid price.");
                return;
            }

            Console.Write("Enter Initial Stock Quantity: ");
            int stock;
            if (!int.TryParse(Console.ReadLine(), out stock) || stock < 0)
            {
                Console.WriteLine("Invalid stock quantity.");
                return;
            }

            bool success = _db.AddProduct(sku, name, categoryId, price, stock);
            if (success)
            {
                Console.WriteLine(string.Format("\n[SUCCESS] Added product '{0}' (SKU: {1}) with {2} units.",
                    name, sku, stock));
            }
            else
            {
                Console.WriteLine("\n[FAILURE] Could not add product. Make sure SKU is unique.");
            }
        }

        static void PlaceCustomerOrder()
        {
            Console.WriteLine("--- Place Customer Sales Order ---");
            Console.WriteLine("Customers:");
            var customers = _db.GetCustomers();
            foreach (var c in customers)
            {
                Console.WriteLine(string.Format("  {0}", c));
            }

            Console.Write("\nEnter Customer ID: ");
            int custId;
            if (!int.TryParse(Console.ReadLine(), out custId)) return;

            Console.WriteLine("\nProducts available:");
            var products = _db.GetProducts();
            foreach (var p in products)
            {
                Console.WriteLine(string.Format("  [{0}] {1} (${2:F2}) - Available: {3}",
                    p.ProductId, p.Name, p.UnitPrice, p.StockQuantity));
            }

            Console.Write("\nEnter Product ID to purchase: ");
            int prodId;
            if (!int.TryParse(Console.ReadLine(), out prodId)) return;

            Console.Write("Enter Quantity: ");
            int qty;
            if (!int.TryParse(Console.ReadLine(), out qty) || qty <= 0) return;

            Console.WriteLine("\nProcessing transaction...");
            var result = _db.PlaceOrder(custId, prodId, qty);

            if (result != null && result.ContainsKey("success") && Convert.ToBoolean(result["success"]))
            {
                Console.WriteLine("--------------------------------------------------");
                Console.WriteLine("[TRANSACTION SUCCESSFUL]");
                Console.WriteLine(string.Format(" Order ID:     #{0}", result["order_id"]));
                Console.WriteLine(string.Format(" Item:         {0}", result["product_name"]));
                Console.WriteLine(string.Format(" Quantity:     {0}", result["quantity"]));
                Console.WriteLine(string.Format(" Unit Price:   ${0:F2}", Convert.ToDecimal(result["unit_price"])));
                Console.WriteLine(string.Format(" Total Paid:   ${0:F2}", Convert.ToDecimal(result["total_amount"])));
                Console.WriteLine(" Stock deducted automatically in SQLite database.");
                Console.WriteLine("--------------------------------------------------");
            }
            else
            {
                string error = result != null && result.ContainsKey("error") ? Convert.ToString(result["error"]) : "Transaction failed.";
                Console.WriteLine(string.Format("[TRANSACTION FAILED] {0}", error));
            }
        }

        static void RestockInventory()
        {
            Console.WriteLine("--- Restock Existing Product ---");
            ListProducts();

            Console.Write("\nEnter Product ID to restock: ");
            int prodId;
            if (!int.TryParse(Console.ReadLine(), out prodId)) return;

            Console.Write("Enter additional units to add: ");
            int units;
            if (!int.TryParse(Console.ReadLine(), out units) || units <= 0) return;

            bool ok = _db.RestockProduct(prodId, units);
            if (ok)
            {
                Console.WriteLine(string.Format("\n[SUCCESS] Added {0} units to Product #{1}.", units, prodId));
            }
            else
            {
                Console.WriteLine("\n[ERROR] Restock update failed.");
            }
        }

        static void ViewOrderHistory()
        {
            Console.WriteLine("--- Order History (Most Recent First) ---");
            Console.WriteLine(new string('-', 75));
            var orders = _db.GetOrders();
            foreach (var o in orders)
            {
                Console.WriteLine(o);
            }
            Console.WriteLine(new string('-', 75));
            Console.WriteLine(string.Format("Total orders recorded: {0}", orders.Count));
        }

        static void RegisterNewCustomer()
        {
            Console.WriteLine("--- Register New Customer / User Account ---");
            Console.Write("Enter Full Name: ");
            string name = Console.ReadLine();
            if (name != null) name = name.Trim();

            Console.Write("Enter Email Address: ");
            string email = Console.ReadLine();
            if (email != null) email = email.Trim().ToLower();

            Console.Write("Enter Password: ");
            string password = Console.ReadLine();
            if (password != null) password = password.Trim();

            Console.Write("Enter City (optional): ");
            string city = Console.ReadLine();
            if (city != null) city = city.Trim();
            if (string.IsNullOrEmpty(city)) city = "Online";

            Console.Write("Enter Phone (optional): ");
            string phone = Console.ReadLine();
            if (phone != null) phone = phone.Trim();

            if (string.IsNullOrEmpty(name) || string.IsNullOrEmpty(email) || string.IsNullOrEmpty(password))
            {
                Console.WriteLine("\n[ERROR] Name, email, and password are required.");
                return;
            }

            var result = _db.RegisterCustomer(name, email, password, city, phone);
            if (result != null && result.ContainsKey("success") && Convert.ToBoolean(result["success"]))
            {
                Console.WriteLine("\n==================================================");
                Console.WriteLine("[SUCCESS] Account created successfully!");
                Console.WriteLine(string.Format("Customer '{0}' registered with Email '{1}'.", name, email));
                Console.WriteLine("Password securely hashed and saved in SQLite.");
                Console.WriteLine("==================================================");
            }
            else
            {
                string err = result != null && result.ContainsKey("error") ? Convert.ToString(result["error"]) : "Registration failed.";
                Console.WriteLine(string.Format("\n[ERROR] {0}", err));
            }
        }

        static void RunCustomSql()
        {
            Console.WriteLine("--- Execute Custom SQL Query ---");
            Console.WriteLine("Example: SELECT sku, name, unit_price FROM products WHERE unit_price > 50");
            Console.Write("Enter SQL: ");
            string sql = Console.ReadLine();
            if (!string.IsNullOrEmpty(sql) && sql.Trim().Length > 0)
            {
                _db.ExecuteCustomSql(sql);
            }
        }

        static void RunDemoMode()
        {
            Console.WriteLine("=== RetailHub .NET Demo Mode ===");
            Console.WriteLine("1. Retrieving Catalog from SQL Database...");
            var products = _db.GetProducts();
            Console.WriteLine(string.Format("Found {0} products in catalog.", products.Count));
            for (int i = 0; i < Math.Min(3, products.Count); i++)
            {
                Console.WriteLine(string.Format("  * {0}", products[i]));
            }

            Console.WriteLine("\n2. Placing an automated demo order (Customer 1 buys 1 Mechanical Keyboard - ID: 2)...");
            var res = _db.PlaceOrder(1, 2, 1);
            if (res != null && res.ContainsKey("success") && Convert.ToBoolean(res["success"]))
            {
                Console.WriteLine(string.Format("  [OK] Order #{0} placed! Product: {1}, Paid: ${2:F2}",
                    res["order_id"], res["product_name"], Convert.ToDecimal(res["total_amount"])));
            }
            else
            {
                Console.WriteLine(string.Format("  [Info] Result: {0}", res != null && res.ContainsKey("error") ? res["error"] : "Failed"));
            }

            Console.WriteLine("\n3. Verifying updated stock levels for Keyboard (ID: 2)...");
            var updated = _db.GetProducts();
            Product kb = updated.Find(delegate(Product p) { return p.ProductId == 2; });
            if (kb != null)
            {
                Console.WriteLine(string.Format("  Updated Stock for {0}: {1} remaining units.", kb.Name, kb.StockQuantity));
            }
            Console.WriteLine("\n=== Demo Complete ===");
        }
    }
}
