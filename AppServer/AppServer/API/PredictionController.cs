using Microsoft.AspNetCore.Mvc;
using AppServer.Models;
using AppServer.Services;
using System.Threading.Tasks;
using AppServer.Models;

namespace AppServer.API
{
    [Route("api/prediction")]
    [ApiController]
    public class PredictionController : ControllerBase
    {
        private readonly PredictionService _predictionService;

        public PredictionController()
        {
            _predictionService = new PredictionService();
        }

        [HttpPost]
        public async Task<IActionResult> PredictFlightDelay([FromBody] Flight_Details flightDetails)
        {
            if (flightDetails == null)
            {
                return BadRequest("Invalid flight details.");
            }

            try
            {
                var prediction = await _predictionService.GetFlightDelayPrediction(flightDetails);

                // Return true if there's a delay (prediction == 1), otherwise false
                bool result = (bool)prediction;

                return Ok(result); // Return boolean value directly
            }
            catch (HttpRequestException ex)
            {
                return StatusCode(500, $"Error calling prediction service: {ex.Message}");
            }
        }

    }
}
