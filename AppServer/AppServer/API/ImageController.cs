using Microsoft.AspNetCore.Mvc;
using AppServer.Services;
using System.Threading.Tasks;

namespace AppServer.API
{
    [ApiController]
    [Route("api/[controller]")]
    public class ImageController : ControllerBase
    {
        private readonly IImaggaService _imaggaService;

        public ImageController(IImaggaService imaggaService)
        {
            _imaggaService = imaggaService;
        }

        // Accepts an image URL in the request body
        [HttpPost("analyze")]
        public async Task<IActionResult> AnalyzeImage([FromBody] string imageUrl)
        {
            if (string.IsNullOrEmpty(imageUrl))
                return BadRequest("Image URL is required.");

            var result = await _imaggaService.AnalyzeImage(imageUrl);

            if (result == null)
                return StatusCode(500, "Error communicating with Imagga.");

            return Ok(result);
        }
    }
}
