using AppServer.Data;
using AppServer.Models;
using Microsoft.EntityFrameworkCore;

public interface IAircraftService
{
    Task AddAircraftAsync(Aircraft aircraft);
    Task DeleteAircraftAsync(int id);
    Task<Aircraft> GetAircraftByIdAsync(int id);
    Task<List<Aircraft>> GetAllAircraftsAsync();
    Task DeleteAllAircraftsAsync();
}

public class AircraftService : IAircraftService
{
    private readonly DBContext _context;

    public AircraftService(DBContext context)
    {
        _context = context;
    }

    // Add a new aircraft
    public async Task AddAircraftAsync(Aircraft aircraft)
    {
        _context.Aircrafts.Add(aircraft);
        await _context.SaveChangesAsync();
    }

    // Delete an aircraft by its Id
    public async Task DeleteAircraftAsync(int id)
    {
        var aircraft = await _context.Aircrafts.FindAsync(id);
        if (aircraft != null)
        {
            _context.Aircrafts.Remove(aircraft);
            await _context.SaveChangesAsync();
        }
    }
    public async Task DeleteAllAircraftsAsync()
    {
        var aircrafts = _context.Aircrafts.ToList();
        _context.Aircrafts.RemoveRange(aircrafts);
        await _context.SaveChangesAsync();
    }

    // Get an aircraft by its Id
    public async Task<Aircraft> GetAircraftByIdAsync(int id)
    {
        return await _context.Aircrafts.FindAsync(id);
    }

    // Get all aircrafts
    public async Task<List<Aircraft>> GetAllAircraftsAsync()
    {
        return await _context.Aircrafts.ToListAsync();
    }
}
