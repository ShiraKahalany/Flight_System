from datetime import datetime
from dal.dal_factory import DALFactory
from models.hebrew_times import DateDetails
from models.flight import Flight

class Utils:
    def __init__(self):
        self.dal = DALFactory.get_instance()
    
    # def validate_aircraft_image(self, image_tags):
    #     valid_tags = ['airplane', 'aircraft', 'plane', 'jet']
    #     return any(tag.lower() in valid_tags for tag in image_tags)

    def check_aircraft_image(self, image_url: str) -> bool:
        return self.dal.ImageRecognition.is_aircraft_image(image_url)

    def get_date_info(self, date: datetime, location: str) -> DateDetails:
        return self.dal.DateDetails.get_date_details(date, location)
    
    @classmethod
    def is_flight_during_shabbat_or_holiday(self, departure: datetime, arrival: datetime, location: str) -> bool:
        departure_info = self.get_date_info(departure, location)
        arrival_info = self.get_date_info(arrival, location)

        return (departure_info.day_of_week==6 or arrival_info.day_of_week==6 or
                departure_info.is_holiday or arrival_info.is_holiday)
    
    @classmethod
    def is_flight_allowed(cls, flight_id) -> bool:
        try:
            flight = self.dal.Flight.get_flight(flight_id)
            departure_info = self.get_date_info(flight.departure_datetime, flight.source)
            arrival_info = self.get_date_info(flight.landing_datetime, flight.destination)
            return (departure_info.day_of_week!=6 and arrival_info.day_of_week!=6 and
                    not departure_info.is_holiday and not arrival_info.is_holiday)
        except Exception as e:
            raise e
            return false


    # def is_flight_allowed(
    #         self, flight:Flight) -> bool:
    #     departure_info = self.get_date_info(flight.departure_datetime, flight.source)
    #     arrival_info = self.get_date_info(flight.landing_datetime, flight.destination)
    #     return (departure_info.day_of_week!=6 and arrival_info.day_of_week!=6 and
    #             not departure_info.is_holiday and not arrival_info.is_holiday)



#     flight_details = {
#     "Season": "Winter",
#     "FlightDistance": 1200,
#     "FlightDuration": 90,
#     "DepartureAirportCongestion": 30,
#     "ArrivalAirportCongestion": 40,
#     "DayOfWeek": "Monday",
#     "TimeOfFlight": "08:00",
#     "ScheduledDepartureTime": "07:30",
#     "ActualDepartureTime": "07:45",
#     "DepartureDelay": 15,
#     "Temperature": 18.5,
#     "Visibility": 10.0,
#     "WindSpeed": 12.3,
#     "WeatherEvent": "Clear"
# }

# # Convert the flight details into a JSON payload
# headers = {'Content-Type': 'application/json'}
# payload = json.dumps(flight_details)

# # Make a POST request to the app server
# try:
#     response = requests.post(app_server_url, data=payload, headers=headers)

#     # Check the response status
#     if response.status_code == 200:
#         # Assuming the response is a simple boolean, print the result
#         is_delayed = response.json()
#         print("Flight Delay Prediction:", "Yes" if is_delayed else "No")
#     else:
#         print(f"Error: Received status code {response.status_code} - {response.text}")

# except requests.exceptions.RequestException as e:
#     print(f"Error occurred while contacting the app server: {e}")v