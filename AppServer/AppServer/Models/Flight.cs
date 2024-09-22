using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace AppServer.Models
{
    public class Flight
    {
        [Key]
        public int Id { get; set; }

        [ForeignKey("Aircraft")]
        [Column("Aircraft_Id")]
        public int AircraftId { get; set; }

        public string Source { get; set; }

        public string Destination { get; set; }

        [Column("Departure_Datetime")]
        public DateTime DepartureDatetime { get; set; }

        [Column("Landing_Datetime")]
        public DateTime LandingDatetime { get; set; }

        [Column("is_delay")]
        public bool IsDelay { get; set; }  

        [Column("price")]
        public decimal Price { get; set; }  
    }
}
