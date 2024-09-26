using AppServer.Models;
using AppServer.Data;
using System.Threading.Tasks;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

public interface ITicketService
{
    Task AddTicketAsync(Ticket ticket);
    Task DeleteTicketAsync(int id);
    Task<Ticket?> GetTicketByIdAsync(int id);
    Task<List<Ticket>> GetAllTicketsAsync();
    Task DeleteAllTicketsAsync();
    Task<IEnumerable<Ticket>> GetTicketsByUserIdAsync(int userId);
}

public class TicketService : ITicketService
{
    private readonly DBContext _context;

    public TicketService(DBContext context)
    {
        _context = context;
    }

    // Add a new ticket
    public async Task AddTicketAsync(Ticket ticket)
    {
        try
        {
            _context.Tickets.Add(ticket);
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateException ex)
        {
            throw new Exception("Database error while adding the ticket.", ex);
        }
    }

    // Delete a ticket by its Id
    public async Task DeleteTicketAsync(int id)
    {
        var ticket = await _context.Tickets.FindAsync(id);
        if (ticket == null)
        {
            throw new KeyNotFoundException($"Ticket with id {id} not found.");
        }

        try
        {
            _context.Tickets.Remove(ticket);
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateException ex)
        {
            throw new Exception("Database error while deleting the ticket.", ex);
        }
    }

    // Delete all tickets
    public async Task DeleteAllTicketsAsync()
    {
        var tickets = await _context.Tickets.ToListAsync();
        if (!tickets.Any())
        {
            throw new KeyNotFoundException("No tickets found.");
        }

        try
        {
            _context.Tickets.RemoveRange(tickets);
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateException ex)
        {
            throw new Exception("Database error while deleting tickets.", ex);
        }
    }

    // Get a ticket by its Id
    public async Task<Ticket?> GetTicketByIdAsync(int id)
    {
        return await _context.Tickets.FindAsync(id);
    }

    // Get all tickets
    public async Task<List<Ticket>> GetAllTicketsAsync()
    {
        return await _context.Tickets.ToListAsync();
    }

    // Get all tickets by user Id
    public async Task<IEnumerable<Ticket>> GetTicketsByUserIdAsync(int userId)
    {
         return await _context.Tickets.Where(t => t.UserId == userId).ToListAsync();
        //if (!tickets.Any())
        //{
        //    throw new KeyNotFoundException($"No tickets found for user {userId}.");
        //}
        //return tickets;
    }
}
