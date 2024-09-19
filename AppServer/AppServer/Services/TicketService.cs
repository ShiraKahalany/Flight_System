using AppServer.Models;
using AppServer.Data;
using System.Threading.Tasks;
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
        _context.Tickets.Add(ticket);  // Add the ticket to the DbSet
        await _context.SaveChangesAsync();  // Save changes to the database
    }

    // Delete a ticket by its Id
    public async Task DeleteTicketAsync(int id)
    {
        var ticket = await _context.Tickets.FindAsync(id);  // Find the ticket by Id
        if (ticket != null)
        {
            _context.Tickets.Remove(ticket);  // Mark the ticket for deletion
            await _context.SaveChangesAsync();  // Commit the changes to the database
        }
    }
    //delete all tickets
    public async Task DeleteAllTicketsAsync()
    {
        var tickets = _context.Tickets.ToList();
        _context.Tickets.RemoveRange(tickets);
        await _context.SaveChangesAsync();
    }

    // Get a ticket by its Id
    public async Task<Ticket?> GetTicketByIdAsync(int id)
    {
        return await _context.Tickets.FindAsync(id);  // Find the ticket by Id
    }

    //Get all Tickets
    public async Task<List<Ticket>> GetAllTicketsAsync()
    {
        return await _context.Tickets.ToListAsync();
    }
    //get all tickets by user id
    public async Task<IEnumerable<Ticket>> GetTicketsByUserIdAsync(int userId)
    {
        return await _context.Tickets.Where(t => t.UserId == userId).ToListAsync();  // Query to get tickets by userId
    }
}
