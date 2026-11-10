namespace RetailHub.Models
{
    /// <summary>
    /// Represents a customer entity.
    /// Demonstrates: C# Encapsulation, Auto-Properties, and Formatting.
    /// </summary>
    public class Customer
    {
        public int CustomerId { get; set; }
        public string FullName { get; set; }
        public string Email { get; set; }
        public string City { get; set; }

        public Customer()
        {
            FullName = string.Empty;
            Email = string.Empty;
            City = string.Empty;
        }

        public Customer(int id, string name, string email, string city)
        {
            CustomerId = id;
            FullName = name;
            Email = email;
            City = city;
        }

        public override string ToString()
        {
            return string.Format("[{0}] {1,-16} | {2,-26} | City: {3}",
                CustomerId, FullName, Email, City);
        }
    }
}
