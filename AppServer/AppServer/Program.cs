using AppServer.Services;
var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// You already have RazorPages; now add support for controllers and HTTP client.
builder.Services.AddRazorPages();
builder.Services.AddControllers(); // This allows you to use API controllers
builder.Services.AddHttpClient();  // This allows you to use HttpClient for external requests

// Register the custom service for Imagga API integration
builder.Services.AddScoped<AppServer.Services.IImaggaService, AppServer.Services.ImaggaService>();

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

// Add this line to map API endpoints
app.MapControllers(); // This ensures that your API controllers (like ImageController) are accessible

// Register Hebcal service
builder.Services.AddScoped<IHebcalService, HebcalService>();

app.Run();

