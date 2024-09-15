using AppServer.Services;
using AppServer.Data;  // Namespace where MyAppContext is located
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddRazorPages();
builder.Services.AddControllers();  // Allows API controllers
builder.Services.AddHttpClient();   // For external API requests

// Register custom services (e.g., ImaggaService, HebcalService)
builder.Services.AddScoped<AppServer.Services.IImaggaService, AppServer.Services.ImaggaService>();
builder.Services.AddScoped<IHebcalService, HebcalService>();

// Register the new custom services for User, Flight, Aircraft, and Ticket
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IFlightService, FlightService>();
builder.Services.AddScoped<IAircraftService, AircraftService>();
builder.Services.AddScoped<ITicketService, TicketService>();

// Register DbContext with SQL Server (replace with your actual connection string)
builder.Services.AddDbContext<DBContext>(options =>
    options.UseSqlServer("workstation id=TSH_FlightDB.mssql.somee.com;packet size=4096;user id=tamar_SQLLogin_2;pwd=qzesmjd7bu;data source=TSH_FlightDB.mssql.somee.com;persist security info=False;initial catalog=TSH_FlightDB;TrustServerCertificate=True"));  // Replace with actual connection string

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();

// Map Razor Pages
app.MapRazorPages();

// Map API endpoints for your controllers
app.MapControllers();  // This ensures that API controllers are accessible

app.Run();
