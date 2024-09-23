using AppServer.Models;
using AppServer.Data;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Threading.Tasks;

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
        try
        {
            _context.Aircrafts.Add(aircraft);
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateException ex)
        {
            throw new Exception("Failed to add aircraft due to a database update error.", ex);
        }
    }

    // Delete an aircraft by its Id
    public async Task DeleteAircraftAsync(int id)
    {
        var aircraft = await _context.Aircrafts.FindAsync(id);
        if (aircraft == null)
        {
            throw new KeyNotFoundException($"Aircraft with id {id} not found.");
        }

        try
        {
            _context.Aircrafts.Remove(aircraft);
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateException ex)
        {
            throw new DbUpdateException("Cannot delete aircraft due to existing associated flights.", ex);
        }
    }

    // Delete all aircrafts
    public async Task DeleteAllAircraftsAsync()
    {
        var aircrafts = await _context.Aircrafts.ToListAsync();
        if (aircrafts == null || aircrafts.Count == 0)
        {
            throw new KeyNotFoundException("No aircrafts found.");
        }

        try
        {
            _context.Aircrafts.RemoveRange(aircrafts);
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateException ex)
        {
            throw new DbUpdateException("Cannot delete aircrafts due to existing associated flights.", ex);
        }
    }

    // Get an aircraft by its Id
    public async Task<Aircraft> GetAircraftByIdAsync(int id)
    {
        var aircraft = await _context.Aircrafts.FindAsync(id);
        if (aircraft == null)
        {
            throw new KeyNotFoundException($"Aircraft with id {id} not found.");
        }
        return aircraft;
    }

    // Get all aircrafts
    public async Task<List<Aircraft>> GetAllAircraftsAsync()
    {
        return await _context.Aircrafts.ToListAsync();
    }
}
