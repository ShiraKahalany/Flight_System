using AppServer.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

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
        await _aircraftService.AddAircraftAsync(aircraft);
        return Ok("Aircraft successfully added");
    }

    // DELETE: api/aircraft/delete/{id}
    [HttpDelete("delete/{id}")]
    public async Task<IActionResult> DeleteAircraft(int id)
    {
        await _aircraftService.DeleteAircraftAsync(id);
        return Ok("Aircraft successfully deleted");
    }


    // DELETE: api/aircraft/delete/all
    [HttpDelete("delete/all")]
    public async Task<IActionResult> DeleteAllAircrafts()
    {
        await _aircraftService.DeleteAllAircraftsAsync();
        return Ok("All aircrafts deleted successfully.");
    }


    // GET: api/aircraft/get/{id}
    [HttpGet("get/{id}")]
    public async Task<IActionResult> GetAircraftById(int id)
    {
        var aircraft = await _aircraftService.GetAircraftByIdAsync(id);
        if (aircraft == null)
        {
            return NotFound();
        }
        return Ok(aircraft);
    }

    // GET: api/aircraft/get/all
    [HttpGet("get/all")]
    public async Task<IActionResult> GetAllAircrafts()
    {
        var aircrafts = await _aircraftService.GetAllAircraftsAsync();
        return Ok(aircrafts);
    }
}
