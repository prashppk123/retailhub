namespace RetailHub.Models
{
    /// <summary>
    /// Represents a customer / registered user entity.
    /// Demonstrates: C# Encapsulation, Auto-Properties, and Formatting.
    /// </summary>
    public class Customer
    {
        public int CustomerId { get; set; }
        public string FullName { get; set; }
        public string Email { get; set; }
        public string City { get; set; }
        public string Role { get; set; }

        public Customer()
        {
            FullName = string.Empty;
            Email = string.Empty;
            City = string.Empty;
            Role = "CUSTOMER";
        }

        public Customer(int id, string name, string email, string city, string role)
        {
            CustomerId = id;
            FullName = name;
            Email = email;
            City = city;
            Role = role;
        }

        public override string ToString()
        {
            return string.Format("[{0}] {1,-18} | {2,-26} | City: {3,-12} | Role: {4}",
                CustomerId, FullName, Email, City, Role);
        }
    }
}
