using Azure.Core;
using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace AppServer.Services
{
    public interface IHebcalService
    {
        Task<string> CheckDate(DateTime date);

    }

    public class HebcalService : IHebcalService
    {
        private readonly HttpClient _httpClient;

        public HebcalService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }
        public async Task<string> CheckDate(DateTime date)
        {
            // Build the Hebcal API URL

            string hebcalApiUrl = $"https://www.hebcal.com/shabbat?cfg=json&geonameid=293397&M=on&gy={date.Year}&gm={date.Month}&gd={date.Day}";


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
