using System;

namespace RetailHub.Models
{
    /// <summary>
    /// Represents a customer sales order.
    /// </summary>
    public class Order
    {
        public int OrderId { get; set; }
        public int CustomerId { get; set; }
        public string CustomerName { get; set; }
        public DateTime OrderDate { get; set; }
        public decimal TotalAmount { get; set; }
        public string Status { get; set; }

        public Order()
        {
            CustomerName = string.Empty;
            Status = "COMPLETED";
            OrderDate = DateTime.Now;
        }

        public override string ToString()
        {
            return string.Format("Order #{0,2} | Date: {1:yyyy-MM-dd HH:mm} | Customer: {2,-16} | Total: ${3,7:F2} | Status: {4}",
                OrderId, OrderDate, CustomerName, TotalAmount, Status);
        }
    }
}
