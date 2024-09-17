import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_data():
    # Get the current script directory
    script_dir = os.path.dirname(__file__)
    
    # Construct the relative path to the CSV file
    csv_file = os.path.join(script_dir, '..', 'data', 'Flight_Delay_Dataset.csv')
    
    # Load the dataset
    df = pd.read_csv(csv_file)

    # Group weather events into two categories: 'Clear' and 'Adverse'
    df['WeatherEvent'] = df['WeatherEvent'].replace({
        'Sunny': 'Clear', 
        'Rain': 'Adverse', 
        'Snow': 'Adverse', 
        'Storm': 'Adverse', 
        'Fog': 'Adverse'
    })

    # Remove WeatherEvent from the features to test the model without it
    df = df.drop(columns=['WeatherEvent'])

    # One-hot encode remaining categorical features (without WeatherEvent)
    categorical_columns = ['Season', 'DayOfWeek']
    df_encoded = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_columns = ['Temperature', 'Visibility', 'WindSpeed', 'FlightDistance', 'FlightDuration', 'DepartureAirportCongestion', 'ArrivalAirportCongestion']
    df_encoded[numerical_columns] = scaler.fit_transform(df_encoded[numerical_columns])
    
    # Split into features (X) and labels (y)
    X = df_encoded.drop(columns=['Delayed', 'ScheduledDepartureTime', 'ActualDepartureTime', 'TimeOfFlight'])
    y = df_encoded['Delayed']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Test preprocessing function
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    print(f"Training set shape: {X_train.shape}")
