# src/predict_service.py

import pickle
import os
import pandas as pd
from preprocess import load_and_preprocess_data

def load_model():
    # Load the trained model from the models directory
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'delay_model.pkl'))
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def predict_delay(flight_data):
    # Load the trained model
    model = load_model()
    
    # Convert flight_data to a pandas DataFrame (to handle single-row predictions)
    flight_df = pd.DataFrame([flight_data])
    
    # Drop columns that were not used during training
    flight_df = flight_df.drop(columns=['ScheduledDepartureTime', 'ActualDepartureTime', 'TimeOfFlight'], errors='ignore')
    
    # One-hot encode categorical features (if needed)
    categorical_columns = ['Season', 'DayOfWeek', 'WeatherEvent']
    flight_df = pd.get_dummies(flight_df, columns=categorical_columns, drop_first=True)

    # Handle missing columns that were in the training data but not in the new data
    expected_columns = model.feature_names_in_
    for col in expected_columns:
        if col not in flight_df.columns:
            flight_df[col] = 0

    # Reorder columns to match training data order
    flight_df = flight_df[expected_columns]
    
    # Use the trained model to make a prediction
    prediction = model.predict(flight_df)
    
    return 'Delayed' if prediction[0] == 1 else 'On Time'

if __name__ == "__main__":
    # Example flight data input (should match the format of your dataset)
    new_flight = {
    "Season": "Winter",
    "FlightDistance": 6000,                  # Arbitrary distance
    "FlightDuration": 1800,                   # Arbitrary duration
    "DepartureAirportCongestion": 10,        # Moderate congestion
    "ArrivalAirportCongestion": 8,           # Moderate congestion
    "DayOfWeek": "Friday",                   # Arbitrary day of the week
    "TimeOfFlight": "14:00:00",              # Arbitrary time of flight
    "ScheduledDepartureTime": "2024-07-15 14:00",
    "ActualDepartureTime": "2024-07-15 14:00", # Departure on time
    "DepartureDelay": 0,                     # No delay
    "Temperature": 25.0,                     # Moderate temperature
    "Visibility": 10000,                     # Good visibility
    "WindSpeed": 5,                          # Low wind speed
    "WeatherEvent": "Adverse"                  # Clear weather
}




    prediction = predict_delay(new_flight)
    print(f"Prediction for the new flight: {prediction}")
