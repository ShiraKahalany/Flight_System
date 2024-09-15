using Microsoft.AspNetCore.Mvc;
using AppServer.Services;
using System;
using System.Threading.Tasks;
using AppServer.Models;
using Newtonsoft.Json;


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

            // Step 1: Fetch the full response from Hebcal API
            var hebcalData = await _hebcalService.checkdate(request.Date);
            var holidayData = await _hebcalService.checkHolyDay(request.Date);
            // Step 2: Deserialize the JSON response
            var jsonData = JsonConvert.DeserializeObject<dynamic>(hebcalData);
            var jsonData2 = JsonConvert.DeserializeObject<dynamic>(holidayData);
            if (jsonData == null)
                return BadRequest("Invalid data from Hebcal API.");
            if (jsonData2 == null)
                return BadRequest("Invalid data from Hebcal API.");
            return Ok(holidayData);
            // Step 3: Extract the required fields from the JSON
            string parsha = null;
            string candleLighting = null;
            string havdalah = null;
            string hebrewDate = null;

            // Loop through the "items" to find Parsha, Candle lighting, and Havdalah
            foreach (var item in jsonData["items"])
            {
                string category = item["category"];
                if (category == "candles")
                {
                    candleLighting = item["title"]; // Candle lighting time
                }
                else if (category == "parashat")
                {
                    parsha = item["hebrew"]; // Parashat Ki Teitzei in Hebrew
                    hebrewDate = item["hdate"]; // Hebrew date, e.g., 11 Elul 5784
                }
                else if (category == "havdalah")
                {
                    havdalah = item["title"]; // Havdalah time
                }
            }

            // Step 4: Create a new MyDate object
            MyDate myDate = new MyDate(
            hebrewDate: hebrewDate,
            gregorianDate: request.Date,
            dayOfWeek: request.Date.DayOfWeek,
            parsha: parsha,
            isHoliday: false,  // Assuming no holiday data in this case
            nextShabbatStart: candleLighting != null ? DateTime.Parse(jsonData["items"][0]["date"].ToString()) : DateTime.MinValue,
            nextShabbatEnd: havdalah != null ? DateTime.Parse(jsonData["items"][2]["date"].ToString()) : DateTime.MinValue,
             holidayStart: null,
            holidayEnd: null
        );


            // Step 5: Return the newly created MyDate object
            return Ok(myDate);
        }


    }
    public class DateRequest
    {
        public DateTime Date { get; set; }
    }
}
