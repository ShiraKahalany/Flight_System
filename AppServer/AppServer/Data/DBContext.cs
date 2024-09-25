using Microsoft.EntityFrameworkCore;
using AppServer.Models;

namespace AppServer.Data
{
    public class DBContext : DbContext
    {
        public DBContext(DbContextOptions<DBContext> options) : base(options) { }

        public DbSet<Ticket> Tickets { get; set; }
        public DbSet<Flight> Flights { get; set; }
        public DbSet<Aircraft> Aircrafts { get; set; }
        public DbSet<User> Users { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseSqlServer(
                    "workstation id=TSH_FlightDB.mssql.somee.com;packet size=4096;user id=tamar_SQLLogin_2;pwd=qzesmjd7bu;data source=TSH_FlightDB.mssql.somee.com;persist security info=False;initial catalog=TSH_FlightDB;TrustServerCertificate=True",
                    sqlServerOptionsAction: sqlOptions =>
                    {
                        sqlOptions.EnableRetryOnFailure(
                            maxRetryCount: 5,  // Retry 5 times
                            maxRetryDelay: TimeSpan.FromSeconds(30),  // Wait up to 30 seconds between retries
                            errorNumbersToAdd: null  // Use default transient errors
                        );
                    });
            }
        }

    }
}
