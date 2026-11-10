namespace RetailHub.Models
{
    /// <summary>
    /// Represents a retail product entity with Indian Rupee (INR - ₹) pricing.
    /// Demonstrates: C# Properties, Constructors, Formatting.
    /// </summary>
    public class Product
    {
        public int ProductId { get; set; }
        public string Sku { get; set; }
        public string Name { get; set; }
        public string Category { get; set; }
        public string ImageUrl { get; set; }
        public decimal UnitPrice { get; set; }
        public int StockQuantity { get; set; }

        public Product()
        {
            Sku = string.Empty;
            Name = string.Empty;
            Category = string.Empty;
            ImageUrl = string.Empty;
        }

        public Product(int id, string sku, string name, string category, string imageUrl, decimal price, int stock)
        {
            ProductId = id;
            Sku = sku;
            Name = name;
            Category = category;
            ImageUrl = imageUrl;
            UnitPrice = price;
            StockQuantity = stock;
        }

        public override string ToString()
        {
            return string.Format("[{0,2}] {1,-9} | {2,-36} | {3,-15} | INR Rs. {4,10:N2} | Stock: {5,3}",
                ProductId, Sku, Name, Category, UnitPrice, StockQuantity);
        }
    }
}
