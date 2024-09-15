using Microsoft.AspNetCore.Mvc;
using AppServer.Services;
using System;
using System.Threading.Tasks;
using AppServer.Models;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;


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

            // Step 1: Call the CheckDate function in the service to get the Hebcal data
            var hebcalData = await _hebcalService.CheckDate(request.Date);

            // Step 2: Deserialize the JSON response
            var jsonData = JsonConvert.DeserializeObject<dynamic>(hebcalData);

            if (jsonData == null)
                return BadRequest("Invalid data from Hebcal API.");

            // Step 3: Extract the relevant fields from the JSON
            string parsha = null;
            string hebrewDate = null;
            string candleLighting = null;
            string havdalah = null;

            // Cast jsonData["items"] to a JArray to handle it as a strongly typed collection
            JArray itemsArray = jsonData["items"] as JArray;

            DateTime nextShabbatStart = DateTime.MinValue;
            DateTime nextShabbatEnd = DateTime.MinValue;

            if (itemsArray != null)
            {
                // Loop through the items to find relevant data
                foreach (var item in itemsArray)
                {
                    string title = (string)item["title"];

                    // Check for candle lighting time
                    if (title.Contains("Candle lighting:"))
                    {
                        candleLighting = title; // Candle lighting time (Shabbat start)
                        if (DateTime.TryParse((string)item["date"], out DateTime parsedDateStart))
                        {
                            nextShabbatStart = parsedDateStart;
                        }
                    }
                    // Check for Havdalah time
                    else if (title.Contains("Havdalah:"))
                    {
                        havdalah = title; // Havdalah time (Shabbat end)
                        if (DateTime.TryParse((string)item["date"], out DateTime parsedDateEnd))
                        {
                            nextShabbatEnd = parsedDateEnd;
                        }
                    }
                    // Check for Parasha information
                    else if (title.Contains("Parashat"))
                    {
                        parsha = (string)item["hebrew"]; // Parasha name
                        hebrewDate = item["hdate"] != null ? (string)item["hdate"] : null; // Hebrew date, e.g., "18 Elul 5784"
                    }
                }
            }

            // Step 5: Create a new MyDate object with the extracted information
            MyDate myDate = new MyDate(
                hebrewDate: hebrewDate,
                gregorianDate: request.Date,
                dayOfWeek: request.Date.DayOfWeek,
                parsha: parsha,
                isHoliday: false, // Not handling holidays for now
                holidayName: null, // No holiday handling
                nextShabbatStart: nextShabbatStart, // Candle lighting time
                nextShabbatEnd: nextShabbatEnd,     // Havdalah time
                holidayStart: null,                 // No holiday
                holidayEnd: null                    // No holiday
            );

            // Step 6: Return the populated MyDate object
            return Ok(myDate);
        }







    }
    public class DateRequest
    {
        public DateTime Date { get; set; }
    }
}
