namespace AppServer.Models;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

public class Aircraft
{
    [Key]
    public int Id { get; set; }

    public string Manufacturer { get; set; }

    public string Nickname { get; set; }

    [Column("Year_of_manufacture")]
    public int YearOfManufacture { get; set; }

    [Column("Image_url")]
    public string ImageUrl { get; set; }

    [Column("Number_of_chairs")]
    public int NumberOfChairs { get; set; }

}
