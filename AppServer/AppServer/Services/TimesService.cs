using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace AppServer.Services
{
    public interface IHebcalService
    {
        Task<string> checkdate(DateTime date);
        Task<string> checkHolyDay(DateTime date);
    }

    public class HebcalService : IHebcalService
    {
        private readonly HttpClient _httpClient;

        public HebcalService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }
        public async Task<string> checkHolyDay(DateTime date)
        {
            string hebcalApiUrl = $"https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&min=on&mod=on&nx=on&year=now&month=x&ss=on&mf=on&c=on&geo=geoname&geonameid=293397&M=on&s=on&gy={date.Year}&gm={date.Month}&gd={date.Day}&g2h=1";


            // Send the GET request to Hebcal API
            HttpResponseMessage response = await _httpClient.GetAsync(hebcalApiUrl); 

            // Check if the response was successful
            if (response.IsSuccessStatusCode)
            {
                // Return the full JSON response as a string
                return await response.Content.ReadAsStringAsync();
            }

            // Handle the case where the API request failed
            throw new HttpRequestException($"Failed to get data from Hebcal. Status code: {response.StatusCode}");
        }
        public async Task<string> checkdate(DateTime date)
        {
            // Build the Hebcal API URL

            string hebcalApiUrl = $"https://www.hebcal.com/shabbat?cfg=json&geonameid=293397&M=on&gy={date.Year}&gm={date.Month}&gd={date.Day}&g2h=1";
        

            // Send the GET request to Hebcal API
            HttpResponseMessage response = await _httpClient.GetAsync(hebcalApiUrl);

            // Check if the response was successful
            if (response.IsSuccessStatusCode)
            {
                // Return the full JSON response as a string
                return await response.Content.ReadAsStringAsync();
            }

            // Handle the case where the API request failed
            throw new HttpRequestException($"Failed to get data from Hebcal. Status code: {response.StatusCode}");
        }
    }
}
