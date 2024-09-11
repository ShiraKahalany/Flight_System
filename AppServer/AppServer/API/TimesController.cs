using Microsoft.AspNetCore.Mvc;
using AppServer.Services;
using AppServer.Models;
using System;
using System.Threading.Tasks;

namespace AppServer.API
{
    [ApiController]
    [Route("api/times")]
    public class HebcalController : ControllerBase
    {
        private readonly IHebcalService _hebcalService;

        public HebcalController(IHebcalService hebcalService)
        {
            _hebcalService = hebcalService;
        }

        [HttpPost("checkdate")]
        public async Task<IActionResult> GetHebcalData([FromBody] DateRequest request)
        {
            if (request?.Date == null)
                return BadRequest("Date is required.");

            // Fetch the full response from Hebcal API
            var hebcalData = await _hebcalService.checkdate(request.Date);

            // Return the full response as a string
            return Ok(hebcalData);
        }
    }
}
