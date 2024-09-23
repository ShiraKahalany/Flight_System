using AppServer.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;

[Route("api/flight")]
[ApiController]
public class FlightController : ControllerBase
{
    private readonly IFlightService _flightService;

    public FlightController(IFlightService flightService)
    {
        _flightService = flightService;
    }

    // POST: api/flight/add
    [HttpPost("add")]
    public async Task<IActionResult> PostFlight([FromBody] Flight flight)
    {
        if (string.IsNullOrEmpty(flight.Source) || string.IsNullOrEmpty(flight.Destination))
        {
            return BadRequest("Source and destination are required.");
        }
        if (flight.DepartureDatetime >= flight.LandingDatetime)
        {
            return BadRequest("Landing time must be after departure time.");
        }
        if (flight.Source == flight.Destination)
        {
            return BadRequest("Source have to be different from the Destination");
        }

        try
        {
            await _flightService.AddFlightAsync(flight);
            return CreatedAtAction(nameof(GetFlightById), new { id = flight.Id }, flight);
        }
        catch (DbUpdateException ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // DELETE: api/flight/delete/{id}
    [HttpDelete("delete/{id}")]
    public async Task<IActionResult> DeleteFlight(int id)
    {
        try
        {
            var flight = await _flightService.GetFlightByIdAsync(id);
            if (flight == null)
            {
                return NotFound($"Flight with id {id} not found.");
            }

            await _flightService.DeleteFlightAsync(id);
            return Ok("Flight successfully deleted.");
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // DELETE: api/flight/delete/all
    [HttpDelete("delete/all")]
    public async Task<IActionResult> DeleteAllFlights()
    {
        try
        {
            await _flightService.DeleteAllFlightsAsync();
            return Ok("All flights deleted successfully.");
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // GET: api/flight/get/{id}
    [HttpGet("get/{id}")]
    public async Task<IActionResult> GetFlightById(int id)
    {
        try
        {
            var flight = await _flightService.GetFlightByIdAsync(id);
            if (flight == null)
            {
                return NotFound($"Flight with id {id} not found.");
            }
            return Ok(flight);
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    [HttpGet("next5hours")]
    public async Task<IActionResult> GetFlightsInNextFiveHours()
    {
        try
        {
            var flights = await _flightService.GetFlightsInNextFiveHoursAsync();
            if (flights == null || !flights.Any())
            {
                return NotFound("No flights departing in the next 5 hours.");
            }

            return Ok(flights);
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // GET: api/flight/get/all
    [HttpGet("get/all")]
    public async Task<IActionResult> GetAllFlights()
    {
        try
        {
            var flights = await _flightService.GetAllFlightsAsync();
            return Ok(flights);
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // GET: api/flight/getbyuser/{userId}
    [HttpGet("getbyuser/{userId}")]
    public async Task<IActionResult> GetFlightsByUserId(int userId)
    {
        try
        {
            var flights = await _flightService.GetFlightsByUserIdAsync(userId);
            if (flights == null || !flights.Any())
            {
                return NotFound($"No flights found for user {userId}.");
            }

            return Ok(flights);
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }
}
