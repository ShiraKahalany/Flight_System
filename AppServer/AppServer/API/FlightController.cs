using AppServer.Models;
using Microsoft.AspNetCore.Mvc;
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
        await _flightService.AddFlightAsync(flight);
        return Ok(flight);
    }

    // DELETE: api/flight/delete/{id}
    [HttpDelete("delete/{id}")]
    public async Task<IActionResult> DeleteFlight(int id)
    {
        await _flightService.DeleteFlightAsync(id);
        return Ok("Flight successfully deleted");
    }

    // DELETE: api/flight/delete/all
    [HttpDelete("delete/all")]
    public async Task<IActionResult> DeleteAllFlights()
    {
        await _flightService.DeleteAllFlightsAsync();
        return Ok("All flights deleted successfully.");
    }

    // GET: api/flight/get/{id}
    [HttpGet("get/{id}")]
    public async Task<IActionResult> GetFlightById(int id)
    {
        var flight = await _flightService.GetFlightByIdAsync(id);
        if (flight == null)
        {
            return NotFound();
        }
        return Ok(flight);
    }

    [HttpGet("next5hours")]
    public async Task<IActionResult> GetFlightsInNextFiveHours()
    {
        var flights = await _flightService.GetFlightsInNextFiveHoursAsync();
        if (flights == null || !flights.Any())
        {
            return NotFound("No flights departing in the next 5 hours.");
        }

        return Ok(flights);
    }

    // GET: api/flight/get/all
    [HttpGet("get/all")]
    public async Task<IActionResult> GetAllFlights()
    {
        var flights = await _flightService.GetAllFlightsAsync();
        return Ok(flights);
    }
    // GET: api/flight/getbyuser/{userId}
    [HttpGet("getbyuser/{userId}")]
    public async Task<IActionResult> GetFlightsByUserId(int userId)
    {
        var flights = await _flightService.GetFlightsByUserIdAsync(userId);
        if (flights == null || !flights.Any())
        {
            return NotFound("No flights found for this user.");
        }

        return Ok(flights);
    }

}

