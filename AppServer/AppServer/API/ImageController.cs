using Microsoft.AspNetCore.Mvc;
using AppServer.Services;
using System.Threading.Tasks;


namespace AppServer.API
{
    [ApiController]
    [Route("api/image")]
    public class ImageController : ControllerBase
    {
        private readonly IImaggaService _imaggaService;

        public ImageController(IImaggaService imaggaService)
        {
            _imaggaService = imaggaService;
        }

        // Accepts an image URL in the request body
        public class ImageRequest
        {
            public string ImageUrl { get; set; }
        }

        [HttpGet("analyze")]
        public async Task<IActionResult> AnalyzeImage([FromBody] ImageRequest request)
        {
            if (string.IsNullOrEmpty(request.ImageUrl))
                return BadRequest("Image URL is required.");

            var result = await _imaggaService.AnalyzeImage(request.ImageUrl);

            if (result == null)
                return StatusCode(500, "Error communicating with Imagga.");

            return Ok(result);
        }

    }
}
