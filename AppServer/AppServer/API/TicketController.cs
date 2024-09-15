using AppServer.Models;
using Microsoft.AspNetCore.Mvc;

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
        await _ticketService.AddTicketAsync(ticket);
        return Ok("Ticket successfully added");
    }

    // DELETE: api/ticket/delete/{id}
    [HttpDelete("delete/{id}")]
    public async Task<IActionResult> DeleteTicket(int id)
    {
        await _ticketService.DeleteTicketAsync(id);
        return Ok("Ticket successfully deleted");
    }

    // DELETE: api/ticket/delete/all
    [HttpDelete("delete/all")]
    public async Task<IActionResult> DeleteAllTickets()
    {
        await _ticketService.DeleteAllTicketsAsync();
        return Ok("All tickets deleted successfully.");
    }

    // GET: api/ticket/get/{id}
    [HttpGet("get/{id}")]
    public async Task<IActionResult> GetTicketById(int id)
    {
        var ticket = await _ticketService.GetTicketByIdAsync(id);
        if (ticket == null)
        {
            return NotFound();
        }
        return Ok(ticket);
    }
    // GET: api/ticket/get/all
    [HttpGet("get/all")]
    public async Task<IActionResult> GetAllFlights()
    {
        var flights = await _ticketService.GetAllTicketsAsync();
        return Ok(flights);
    }
}
