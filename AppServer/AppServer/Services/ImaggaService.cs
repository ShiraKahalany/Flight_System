using System.Text;
using System.Net.Http;
using System.Threading.Tasks;

namespace AppServer.Services
{
    public interface IImaggaService
    {
        Task<string> AnalyzeImage(string imageUrl);
    }

    public class ImaggaService : IImaggaService
    {
        private readonly HttpClient _httpClient;

        public ImaggaService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<string> AnalyzeImage(string imageUrl)
        {
            string apiKey = "acc_aad59a8339accd0";
            string apiSecret = "553135ac9f01ee8f19c339d546f14309";

            // Construct Basic Auth string (Base64 encoding of "apiKey:apiSecret")
            string credentials = $"{apiKey}:{apiSecret}";
            string encodedCredentials = Convert.ToBase64String(Encoding.UTF8.GetBytes(credentials));

            // Build the Imagga API endpoint for image URL analysis
            string endpointUrl = "https://api.imagga.com/v2/tags";
            string requestUrl = $"{endpointUrl}?image_url={imageUrl}";

            // Prepare the request with Authorization header
            var request = new HttpRequestMessage(HttpMethod.Get, requestUrl);
            request.Headers.Add("Authorization", $"Basic {encodedCredentials}");

            // Send the GET request to Imagga API
            HttpResponseMessage response = await _httpClient.SendAsync(request);

            // Check if the response was successful
            if (response.IsSuccessStatusCode)
            {
                // Read the response content as a string
                string jsonResponse = await response.Content.ReadAsStringAsync();
                return jsonResponse;
            }
            else
            {
                // Handle the error (e.g., throw an exception or return an error message)
                throw new HttpRequestException($"Failed to analyze image. Status code: {response.StatusCode}");
            }
        }
    }
}
