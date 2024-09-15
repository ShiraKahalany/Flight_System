using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace AppServer.Models
{
    public class Ticket
    {
        [Key]
        [Column("Id")]  // Map the Id property to the 'id' column in the database
        public int Id { get; set; }


        [Column("User_Id")]  // Map the UserId property to the 'user_id' column
        public int UserId { get; set; }


        [Column("Flight_Id")]  // Map the FlightId property to the 'flight_id' column
        public int FlightId { get; set; }

        [Column("purchase_datetime")]  // Map the PurchaseDatetime property to the 'purchase_datetime' column
        public DateTime PurchaseDatetime { get; set; }
    }
}
