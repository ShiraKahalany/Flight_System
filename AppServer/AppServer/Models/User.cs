namespace AppServer.Models;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

public class User
{
    [Key]
    public int Id { get; set; }

    public string Username { get; set; }

    public string Password { get; set; }

    public string Role { get; set; }  // 'admin' or 'passenger'

    [Column("First_Name")]
    public string FirstName { get; set; }

    [Column("Last_Name")]
    public string LastName { get; set; }

    public string Email { get; set; }

}
