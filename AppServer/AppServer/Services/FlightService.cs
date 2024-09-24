using AppServer.Models;
using AppServer.Data;
using System.Threading.Tasks;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

public interface IFlightService
{
    Task AddFlightAsync(Flight flight);
    Task DeleteFlightAsync(int id);
    Task<Flight?> GetFlightByIdAsync(int id);
    Task<List<Flight>> GetAllFlightsAsync();
    Task<List<Flight>> GetFlightsInNextFiveHoursAsync();
    Task<List<Flight>> GetFlightsByUserIdAsync(int userId);
    Task DeleteAllFlightsAsync();
}

public class FlightService : IFlightService
{
    private readonly DBContext _context;

    public FlightService(DBContext context)
    {
        _context = context;
    }

    // Add a new flight
    public async Task AddFlightAsync(Flight flight)
    {
        if (flight.DepartureDatetime >= flight.LandingDatetime)
        {
            throw new ArgumentException("Landing time must be after departure time.");
        }

        try
        {
            _context.Flights.Add(flight);
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateException ex)
        {
            throw new Exception("Database update failed", ex);
        }
    }

    // Delete a flight by its Id
    public async Task DeleteFlightAsync(int id)
    {
        var flight = await _context.Flights.FindAsync(id);
        if (flight == null)
        {
            throw new KeyNotFoundException($"Flight with id {id} not found.");
        }
        _context.Flights.Remove(flight);
        await _context.SaveChangesAsync();
    }

    // Delete all flights
    public async Task DeleteAllFlightsAsync()
    {
        var flights = await _context.Flights.ToListAsync();
        _context.Flights.RemoveRange(flights);
        await _context.SaveChangesAsync();
    }

    // Get a flight by its Id
    public async Task<Flight?> GetFlightByIdAsync(int id)
    {
        return await _context.Flights.FindAsync(id);
    }

    // Get all flights
    public async Task<List<Flight>> GetAllFlightsAsync()
    {
        return await _context.Flights.Where(f => f.LandingDatetime > DateTime.Now).ToListAsync();
    }

    // Get flights in the next 5 hours
    public async Task<List<Flight>> GetFlightsInNextFiveHoursAsync()
    {
        DateTime currentTime = DateTime.Now;
        DateTime endTime = currentTime.AddHours(5);

        return await _context.Flights
            .Where(f =>f.Destination=="Tel Aviv" && f.LandingDatetime >= currentTime && f.LandingDatetime <= endTime)
            .ToListAsync();
    }

    // Get flights by user Id
    public async Task<List<Flight>> GetFlightsByUserIdAsync(int userId)
    {
        return await (from ticket in _context.Tickets
                      join flight in _context.Flights
                      on ticket.FlightId equals flight.Id
                      where ticket.UserId == userId
                      select flight).ToListAsync();
    }
}
