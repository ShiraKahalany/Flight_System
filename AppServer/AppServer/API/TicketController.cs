using AppServer.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;

[Route("api/ticket")]
[ApiController]
public class TicketController : ControllerBase
{
    private readonly ITicketService _ticketService;

    public TicketController(ITicketService ticketService)
    {
        _ticketService = ticketService;
    }

    // POST: api/ticket/add
    [HttpPost("add")]
    public async Task<IActionResult> AddTicket([FromBody] Ticket ticket)
    {
        if (ticket.UserId == 0 || ticket.FlightId == 0)
        {
            return BadRequest("UserId and FlightId are required.");
        }

        try
        {
            await _ticketService.AddTicketAsync(ticket);
            return CreatedAtAction(nameof(GetTicketById), new { id = ticket.Id }, ticket);
        }
        catch (DbUpdateException ex)
        {
            return Conflict($"Error adding the ticket: {ex.Message}");
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // DELETE: api/ticket/delete/{id}
    [HttpDelete("delete/{id}")]
    public async Task<IActionResult> DeleteTicket(int id)
    {
        try
        {
            var ticket = await _ticketService.GetTicketByIdAsync(id);
            if (ticket == null)
            {
                return NotFound($"Ticket with id {id} not found.");
            }

            await _ticketService.DeleteTicketAsync(id);
            return Ok("Ticket successfully deleted.");
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // DELETE: api/ticket/delete/all
    [HttpDelete("delete/all")]
    public async Task<IActionResult> DeleteAllTickets()
    {
        try
        {
            await _ticketService.DeleteAllTicketsAsync();
            return Ok("All tickets deleted successfully.");
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // GET: api/ticket/get/{id}
    [HttpGet("get/{id}")]
    public async Task<IActionResult> GetTicketById(int id)
    {
        try
        {
            var ticket = await _ticketService.GetTicketByIdAsync(id);
            if (ticket == null)
            {
                return NotFound($"Ticket with id {id} not found.");
            }
            return Ok(ticket);
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // GET: api/ticket/get/all
    [HttpGet("get/all")]
    public async Task<IActionResult> GetAllTickets()
    {
        try
        {
            var tickets = await _ticketService.GetAllTicketsAsync();
            return Ok(tickets);
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // GET: api/ticket/getbyuser/{userId}
    [HttpGet("getbyuser/{userId}")]
    public async Task<IActionResult> GetTicketsByUserId(int userId)
    {
        try
        {
            var tickets = await _ticketService.GetTicketsByUserIdAsync(userId);
            return Ok(tickets);
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }
}
