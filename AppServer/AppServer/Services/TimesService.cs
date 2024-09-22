using Azure.Core;
using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace AppServer.Services
{
    public interface IHebcalService
    {
        Task<string> CheckDate(DateTime date, int choose, int location = 293397);

    }

    public class HebcalService : IHebcalService
    {
        private readonly HttpClient _httpClient;

        public HebcalService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }
        public async Task<string> CheckDate(DateTime date, int choose,int location = 293397)
        {
            string hebcalApiUrl;
            // Build the Hebcal API URL
            if (choose == 0)
            {
                //shabbat times
                hebcalApiUrl = $"https://www.hebcal.com/shabbat?cfg=json&geonameid={location}&M=on&gy={date.Year}&gm={date.Month}&gd={date.Day}";
            }
            else
            {
                //hebrew date
                string dateString = date.ToString("yyyy-MM-ddTHH:mm:ss");
                hebcalApiUrl = $"https://www.hebcal.com/converter?cfg=json&date={dateString}&g2h=1&strict=1";
            }
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
