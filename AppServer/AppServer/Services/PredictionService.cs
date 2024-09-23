using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using AppServer.Models;

namespace AppServer.Services
{
    public class PredictionService
    {
        private readonly HttpClient _httpClient;
        private readonly string _predictionApiUrl = "http://localhost:5000/predict";  // Update this URL if needed

        public PredictionService()
        {
            _httpClient = new HttpClient();
        }

        // The method returns a bool directly
        public async Task<bool> GetFlightDelayPrediction(Flight_Details flightDetails)
        {
            var jsonContent = JsonConvert.SerializeObject(flightDetails);
            var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync(_predictionApiUrl, content);

            if (response.IsSuccessStatusCode)
            {
                var responseBody = await response.Content.ReadAsStringAsync();

                // Deserialize the prediction field directly
                var result = JsonConvert.DeserializeObject<dynamic>(responseBody);

                // Check if the prediction is 1 (delay), then return true; otherwise false
                return result.prediction == 1;
            }
            else
            {
                throw new HttpRequestException("Failed to get prediction from the prediction service.");
            }
        }
    }
}
