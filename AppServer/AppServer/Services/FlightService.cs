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
        _context.Flights.Add(flight);
        await _context.SaveChangesAsync();
    }

    // Delete a flight by its Id
    public async Task DeleteFlightAsync(int id)
    {
        var flight = await _context.Flights.FindAsync(id);
        if (flight != null)
        {
            _context.Flights.Remove(flight);
            await _context.SaveChangesAsync();
        }
    }

    //delete all flights
    public async Task DeleteAllFlightsAsync()
    {
        var flights = _context.Flights.ToList();
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
        return await _context.Flights.Where(f => f.LandingDatetime>DateTime.Now).ToListAsync();
    }
    //get flights from next 5 hours
    public async Task<List<Flight>> GetFlightsInNextFiveHoursAsync()
    {
        DateTime currentTime = DateTime.Now;
        DateTime endTime = currentTime.AddHours(5);

        // Query to fetch flights departing in the next 5 hours
        return await _context.Flights
            .Where(f =>f.Destination=="Tel-Aviv" && f.LandingDatetime >= currentTime && f.LandingDatetime <= endTime)
            .ToListAsync();
    }

    public async Task<List<Flight>> GetFlightsByUserIdAsync(int userId)
    {
        // Step 1: Retrieve all tickets for the given user
        var flights = await (from ticket in _context.Tickets
                             join flight in _context.Flights
                             on ticket.FlightId equals flight.Id
                             where ticket.UserId == userId
                             select flight).ToListAsync();

        return flights;

    }
}
