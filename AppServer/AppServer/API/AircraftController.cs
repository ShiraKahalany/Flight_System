using AppServer.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;

[Route("api/aircraft")]
[ApiController]
public class AircraftController : ControllerBase
{
    private readonly IAircraftService _aircraftService;

    public AircraftController(IAircraftService aircraftService)
    {
        _aircraftService = aircraftService;
    }

    // POST: api/aircraft/add
    [HttpPost("add")]
    public async Task<IActionResult> PostAircraft([FromBody] Aircraft aircraft)
    {
        // Validate required fields
        if (string.IsNullOrEmpty(aircraft.Manufacturer) || string.IsNullOrEmpty(aircraft.Nickname))
        {
            return BadRequest("Manufacturer and Nickname are required.");
        }

        try
        {
            await _aircraftService.AddAircraftAsync(aircraft);
            return CreatedAtAction(nameof(GetAircraftById), new { id = aircraft.Id }, aircraft);
        }
        catch (DbUpdateException ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // DELETE: api/aircraft/delete/{id}
    [HttpDelete("delete/{id}")]
    public async Task<IActionResult> DeleteAircraft(int id)
    {
        try
        {
            var aircraft = await _aircraftService.GetAircraftByIdAsync(id);
            if (aircraft == null)
            {
                return NotFound($"Aircraft with id {id} not found.");
            }

            await _aircraftService.DeleteAircraftAsync(id);
            return Ok("Aircraft successfully deleted.");
        }
        catch (DbUpdateException ex)
        {
            return Conflict($"Cannot delete aircraft with id {id}, as it is associated with existing flights.");
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // DELETE: api/aircraft/delete/all
    [HttpDelete("delete/all")]
    public async Task<IActionResult> DeleteAllAircrafts()
    {
        try
        {
            await _aircraftService.DeleteAllAircraftsAsync();
            return Ok("All aircrafts deleted successfully.");
        }
        catch (DbUpdateException ex)
        {
            return Conflict($"Cannot delete all aircrafts, as some are associated with existing flights.");
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // GET: api/aircraft/get/{id}
    [HttpGet("get/{id}")]
    public async Task<IActionResult> GetAircraftById(int id)
    {
        try
        {
            var aircraft = await _aircraftService.GetAircraftByIdAsync(id);
            if (aircraft == null)
            {
                return NotFound($"Aircraft with id {id} not found.");
            }
            return Ok(aircraft);
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    // GET: api/aircraft/get/all
    [HttpGet("get/all")]
    public async Task<IActionResult> GetAllAircrafts()
    {
        try
        {
            var aircrafts = await _aircraftService.GetAllAircraftsAsync();
            return Ok(aircrafts);
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }
}
