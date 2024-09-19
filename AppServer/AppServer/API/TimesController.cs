using Microsoft.AspNetCore.Mvc;
using AppServer.Services;
using System;
using System.Threading.Tasks;
using AppServer.Models;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Globalization;


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
            var TimesData = await _hebcalService.CheckDate(request.Date,0,request.Location);
            var DateData = await _hebcalService.CheckDate(request.Date,1,request.Location);
            //return Ok(TimesData);
            // Step 2: Deserialize the JSON response
            var jsonDate = JsonConvert.DeserializeObject<dynamic>(DateData);
            var jsonTimes = JsonConvert.DeserializeObject<dynamic>(TimesData);

            if (jsonDate == null|| jsonTimes==null)
                return BadRequest("Invalid data from Hebcal API.");

            // Step 3: Extract the relevant fields from the JSON
            string parsha = null;
            string hebrewDate = jsonDate["hebrew"] ?? null; // Hebrew date
            string candleLighting = null;
            string havdalah = null;
            bool isHoliday = false;
            DateTime currentDate=DateTime.Now;

            // Cast jsonData["items"] to a JArray to handle it as a strongly typed collection
            JArray itemsArray = jsonTimes["items"] as JArray;

            DateTime nextShabbatStart = DateTime.MinValue;
            DateTime nextShabbatEnd = DateTime.MinValue;

            string format = "MM/dd/yyyy HH:mm:ss";

            if (itemsArray != null)
            {
                // Loop through the items to find relevant data
                foreach (var item in itemsArray)
                {
                    string title = (string)item["title"];

                    // Check for candle lighting time
                    if (title.Contains("Candle lighting:"))
                    {
                        candleLighting = (string)item["date"]; // Candle lighting time (Shabbat start)

                        if (DateTime.TryParseExact(candleLighting, format, CultureInfo.InvariantCulture, DateTimeStyles.None, out DateTime parsedDateStart))
                        {
                            nextShabbatStart = parsedDateStart; // Successfully parsed date
                        }
                    }
                    // Check for Havdalah time
                    else if (title.Contains("Havdalah:"))
                    {
                        havdalah = (string)item["date"]; // Havdalah time (Shabbat end)

                        if (DateTime.TryParseExact(havdalah, format, CultureInfo.InvariantCulture, DateTimeStyles.None, out DateTime parsedDateEnd))
                        {
                            nextShabbatEnd = parsedDateEnd;
                        }
                       
                    }
                    //check if holiday
                    string datetime = (string)item["date"];
                    
                    if (DateTime.TryParseExact(datetime, format, CultureInfo.InvariantCulture, DateTimeStyles.None, out DateTime parsedDate))
                    {
                        currentDate = parsedDate;
                    }
                    else if (item["yomtov"] != null && (bool)item["yomtov"] == true && currentDate.Date == request.Date.Date)
                    {
                        isHoliday = true; // Set IsHoliday to true if yomtov is present and true
                    }
                    // Check for Parasha information
                    else if (title.Contains("Parashat"))
                    {
                        parsha = (string)item["hebrew"]; // Parasha name
                    }
                }
            }

            // Step 5: Create a new MyDate object with the extracted information
            MyDate myDate = new MyDate(
                hebrewDate: hebrewDate,
                gregorianDate: request.Date,
                dayOfWeek: request.Date.DayOfWeek,
                parsha: parsha,
                isHoliday: isHoliday, // Not handling holidays for now
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
        public int Location {  get; set; }
    }
}
