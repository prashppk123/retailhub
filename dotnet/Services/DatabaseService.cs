using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Web.Script.Serialization;
using RetailHub.Models;

namespace RetailHub.Services
{
    /// <summary>
    /// Service layer handling business logic and SQL execution.
    /// Demonstrates:
    ///  - Process Execution & Inter-Process Communication (IPC)
    ///  - SQL Statement execution & Parameter sanitization
    ///  - JSON Deserialization into Strongly-Typed C# Models
    ///  - Error Handling & Transaction feedback
    /// </summary>
    public class DatabaseService
    {
        private readonly string _pythonExe;
        private readonly string _bridgeScript;
        private readonly JavaScriptSerializer _serializer;

        public DatabaseService()
        {
            _serializer = new JavaScriptSerializer();

            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            string projectRoot = Directory.Exists(Path.Combine(baseDir, "python"))
                ? baseDir
                : Path.GetFullPath(Path.Combine(baseDir, @"..\..\"));

            if (!Directory.Exists(Path.Combine(projectRoot, "python")))
            {
                projectRoot = @"C:\Users\prash\.gemini\antigravity\scratch\retail_analytics_hub";
            }

            _bridgeScript = Path.Combine(projectRoot, "python", "db_bridge.py");

            string localPython = @"C:\Users\prash\AppData\Local\Programs\Python\Python315\python.exe";
            _pythonExe = File.Exists(localPython) ? localPython : "python";
        }

        private string RunBridge(string arguments)
        {
            var psi = new ProcessStartInfo
            {
                FileName = _pythonExe,
                Arguments = string.Format("\"{0}\" {1}", _bridgeScript, arguments),
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (var process = Process.Start(psi))
            {
                if (process == null) throw new Exception("Failed to start database bridge process.");
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                process.WaitForExit();

                if (!string.IsNullOrEmpty(error) && string.IsNullOrEmpty(output))
                {
                    throw new Exception("Bridge error: " + error);
                }
                return output.Trim();
            }
        }

        public List<Product> GetProducts()
        {
            var list = new List<Product>();
            string sql = "SELECT p.product_id, p.sku, p.name, c.name AS category, p.unit_price, p.stock_quantity FROM products p JOIN categories c ON p.category_id = c.category_id WHERE p.is_active = 1 ORDER BY p.product_id";
            string json = RunBridge(string.Format("query \"{0}\"", sql));

            var root = _serializer.Deserialize<Dictionary<string, object>>(json);
            if (root != null && root.ContainsKey("data"))
            {
                var rows = root["data"] as ArrayList;
                if (rows != null)
                {
                    foreach (Dictionary<string, object> row in rows)
                    {
                        list.Add(new Product(
                            Convert.ToInt32(row["product_id"]),
                            Convert.ToString(row["sku"]),
                            Convert.ToString(row["name"]),
                            Convert.ToString(row["category"]),
                            Convert.ToDecimal(row["unit_price"]),
                            Convert.ToInt32(row["stock_quantity"])
                        ));
                    }
                }
            }
            return list;
        }

        public List<Customer> GetCustomers()
        {
            var list = new List<Customer>();
            string sql = "SELECT customer_id, full_name, email, city, role FROM customers ORDER BY customer_id";
            string json = RunBridge(string.Format("query \"{0}\"", sql));

            var root = _serializer.Deserialize<Dictionary<string, object>>(json);
            if (root != null && root.ContainsKey("data"))
            {
                var rows = root["data"] as ArrayList;
                if (rows != null)
                {
                    foreach (Dictionary<string, object> row in rows)
                    {
                        list.Add(new Customer(
                            Convert.ToInt32(row["customer_id"]),
                            Convert.ToString(row["full_name"]),
                            Convert.ToString(row["email"]),
                            Convert.ToString(row["city"]),
                            row.ContainsKey("role") ? Convert.ToString(row["role"]) : "CUSTOMER"
                        ));
                    }
                }
            }
            return list;
        }

        public Dictionary<string, object> RegisterCustomer(string fullName, string email, string password, string city, string phone)
        {
            string safeName = fullName.Replace("\"", "");
            string safeEmail = email.Replace("\"", "");
            string safePwd = password.Replace("\"", "");
            string safeCity = string.IsNullOrEmpty(city) ? "Online" : city.Replace("\"", "");
            string safePhone = string.IsNullOrEmpty(phone) ? "" : phone.Replace("\"", "");

            string json = RunBridge(string.Format("register \"{0}\" \"{1}\" \"{2}\" \"{3}\" \"{4}\"",
                safeName, safeEmail, safePwd, safeCity, safePhone));
            return _serializer.Deserialize<Dictionary<string, object>>(json);
        }

        public List<Order> GetOrders()
        {
            var list = new List<Order>();
            string sql = "SELECT o.order_id, o.customer_id, c.full_name AS customer_name, o.order_date, o.total_amount, o.status FROM orders o JOIN customers c ON o.customer_id = c.customer_id ORDER BY o.order_id DESC";
            string json = RunBridge(string.Format("query \"{0}\"", sql));

            var root = _serializer.Deserialize<Dictionary<string, object>>(json);
            if (root != null && root.ContainsKey("data"))
            {
                var rows = root["data"] as ArrayList;
                if (rows != null)
                {
                    foreach (Dictionary<string, object> row in rows)
                    {
                        DateTime date;
                        if (!DateTime.TryParse(Convert.ToString(row["order_date"]), out date))
                        {
                            date = DateTime.Now;
                        }

                        list.Add(new Order
                        {
                            OrderId = Convert.ToInt32(row["order_id"]),
                            CustomerId = Convert.ToInt32(row["customer_id"]),
                            CustomerName = Convert.ToString(row["customer_name"]),
                            OrderDate = date,
                            TotalAmount = Convert.ToDecimal(row["total_amount"]),
                            Status = Convert.ToString(row["status"])
                        });
                    }
                }
            }
            return list;
        }

        public bool AddProduct(string sku, string name, int categoryId, decimal price, int stock)
        {
            string safeName = name.Replace("'", "''");
            string safeSku = sku.Replace("'", "''");
            string sql = string.Format("INSERT INTO products (sku, name, category_id, unit_price, stock_quantity, is_active) VALUES ('{0}', '{1}', {2}, {3}, {4}, 1)",
                safeSku, safeName, categoryId, price, stock);
            string json = RunBridge(string.Format("execute \"{0}\"", sql));

            var root = _serializer.Deserialize<Dictionary<string, object>>(json);
            return root != null && root.ContainsKey("success") && Convert.ToBoolean(root["success"]);
        }

        public bool RestockProduct(int productId, int additionalUnits)
        {
            string sql = string.Format("UPDATE products SET stock_quantity = stock_quantity + {0} WHERE product_id = {1}",
                additionalUnits, productId);
            string json = RunBridge(string.Format("execute \"{0}\"", sql));

            var root = _serializer.Deserialize<Dictionary<string, object>>(json);
            return root != null && root.ContainsKey("success") && Convert.ToBoolean(root["success"]);
        }

        public Dictionary<string, object> PlaceOrder(int customerId, int productId, int quantity)
        {
            string json = RunBridge(string.Format("order {0} {1} {2}", customerId, productId, quantity));
            return _serializer.Deserialize<Dictionary<string, object>>(json);
        }

        public void ExecuteCustomSql(string sql)
        {
            string json = RunBridge(string.Format("query \"{0}\"", sql));
            var root = _serializer.Deserialize<Dictionary<string, object>>(json);
            if (root != null && root.ContainsKey("success") && Convert.ToBoolean(root["success"]))
            {
                var rows = root["data"] as ArrayList;
                if (rows == null || rows.Count == 0)
                {
                    Console.WriteLine("Query executed successfully. 0 rows returned.");
                    return;
                }

                Console.WriteLine(string.Format("\n--- Query Result ({0} rows) ---", rows.Count));
                var firstRow = rows[0] as Dictionary<string, object>;
                if (firstRow != null)
                {
                    foreach (var key in firstRow.Keys)
                    {
                        Console.Write(string.Format("{0,-20} | ", key));
                    }
                    Console.WriteLine("\n" + new string('-', firstRow.Keys.Count * 23));

                    foreach (Dictionary<string, object> row in rows)
                    {
                        foreach (var val in row.Values)
                        {
                            Console.Write(string.Format("{0,-20} | ", Convert.ToString(val)));
                        }
                        Console.WriteLine();
                    }
                }
            }
            else
            {
                string error = root != null && root.ContainsKey("error") ? Convert.ToString(root["error"]) : "Unknown error";
                Console.WriteLine(string.Format("[SQL Error] {0}", error));
            }
        }
    }
}
