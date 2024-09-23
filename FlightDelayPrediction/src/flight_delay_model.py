import pandas as pd
import numpy as np  # Make sure to import numpy
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
file_path = "FlightDelayPrediction/data/Updated_Flight_Delay_Dataset.csv"
df = pd.read_csv(file_path)

# Preprocessing: Encode categorical columns
categorical_columns = df.select_dtypes(include=['object']).columns
label_encoders = {}

# Encode all categorical columns
for column in categorical_columns:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column])

# Split the data into features and target
X = df.drop(columns=['Delayed'])  # Features
y = df['Delayed']  # Target

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=200, random_state=42)
rf_classifier.fit(X_train_scaled, y_train)

# Test the model on the testing data
y_pred_rf_test = rf_classifier.predict(X_test_scaled)
accuracy_rf_test = accuracy_score(y_test, y_pred_rf_test)
classification_report_rf_test = classification_report(y_test, y_pred_rf_test)

# Print the accuracy and classification report
print("Accuracy:", accuracy_rf_test)
print("Classification Report:\n", classification_report_rf_test)


# Function to predict if the flight will be delayed (0 or 1)
def predict_flight_delay(new_data):
    # Convert new_data to DataFrame (wrap it in a list to ensure it's 2D)
    new_data_df = pd.DataFrame([new_data])

    # Preprocess the new data: encoding and scaling
    for column in categorical_columns:
        if column in new_data_df:
            le = label_encoders[column]
            le_classes = le.classes_

            # Find unseen labels in the new_data and extend the classes
            unseen_labels = set(new_data_df[column]) - set(le_classes)
            if unseen_labels:
                print(f"Unseen labels detected in column '{column}': {unseen_labels}. Extending label encoder.")
                le.classes_ = np.concatenate([le_classes, list(unseen_labels)])

            # Transform using the extended label encoder
            new_data_df[column] = le.transform(new_data_df[column])

    # Scale the data
    new_data_scaled = scaler.transform(new_data_df)

    # Predict and return the result (0 or 1)
    prediction = rf_classifier.predict(new_data_scaled)

    return prediction[0]  # Since we predict a single sample, return the first (and only) result



# Example usage: predicting for new landing data
# new_landing = pd.DataFrame({
#     'Season': ['Winter'],
#     'FlightDistance': [1200],
#     'FlightDuration': [90],
#     'DepartureAirportCongestion': [30],
#     'ArrivalAirportCongestion': [40],
#     'DayOfWeek': ['Monday'],
#     'TimeOfFlight': ['08:00'],
#     'ScheduledDepartureTime': ['07:30'],
#     'ActualDepartureTime': ['07:45'],
#     'DepartureDelay': [15],
#     'Temperature': [18.5],
#     'Visibility': [10],
#     'WindSpeed': [12.3],
#     'WeatherEvent': ['Clear']
# })

# prediction = predict_flight_delay(new_landing)
# print("Prediction (0 = not delayed, 1 = delayed):", prediction[0])
