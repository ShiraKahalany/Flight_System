from flask import Flask, request, jsonify
from flight_delay_model import predict_flight_delay  # Import the prediction function

# Initialize Flask app
app = Flask(__name__)

# Define a route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse incoming JSON request
        flight_data = request.json

        # Ensure required fields are present
        required_fields = [
            'Season', 'FlightDistance', 'FlightDuration', 'DepartureAirportCongestion', 'ArrivalAirportCongestion',
            'DayOfWeek', 'TimeOfFlight', 'ScheduledDepartureTime', 'ActualDepartureTime', 'DepartureDelay',
            'Temperature', 'Visibility', 'WindSpeed', 'WeatherEvent'
        ]
        
        # Check if all required fields are present in the input
        missing_fields = [field for field in required_fields if field not in flight_data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        # Call the predict function with the input data
        prediction = predict_flight_delay(flight_data)

        # Return the prediction
        return jsonify({
            'prediction': int(prediction),
            'description': '0 = No delay, 1 = Delay'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
