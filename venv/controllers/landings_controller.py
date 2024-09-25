from PySide6.QtWidgets import QMessageBox
from Flight_View.landings_view import LandingsView
from exceptions import FlightRetrievalException, NetworkException, UnexpectedErrorException
from datetime import datetime, timedelta
import random

class LandingsController:
    def __init__(self, main_controller, dal):
        self.main_controller = main_controller
        self.dal = dal

    def watch_landings(self):
        try:
            flights_in_next_5_hours = self.dal.Flight.get_BGR_lands_next_5_hours()
            landings_view = LandingsView(controller=self)
            self.main_controller.set_view(landings_view)
        except Exception as e:
            self.show_error_message(f"Error fetching landings: {e}")

    def get_upcoming_landings(self, hours_ahead):
        try:
            flights_in_next_5_hours = self.dal.Flight.get_BGR_lands_next_5_hours()
            now = datetime.now()
            future_time = now + timedelta(hours=hours_ahead)
            filtered_flights = [f for f in flights_in_next_5_hours if now <= f.landing_datetime <= future_time]
            return filtered_flights
        except Exception as e:
            self.show_error_message(f"Error retrieving upcoming landings: {e}")
            return []

    def predict_landing_delay(self, flight):
        distance_map = {
            "New York": 9160, "London": 3580, "Tokyo": 9920, "Paris": 3310, "Los Angeles": 12070,
            "Dubai": 2120, "Singapore": 8130, "Hong Kong": 8050, "Sydney": 13850, "Toronto": 9000,
            "Berlin": 2920, "Amsterdam": 3320, "Bangkok": 7180, "Istanbul": 1120, "Moscow": 2670,
            "Mumbai": 4080, "São Paulo": 10100, "Mexico City": 12450, "Johannesburg": 7090,
            "Cairo": 410, "Delhi": 4050, "Rome": 2300, "Madrid": 3670, "Frankfurt": 3050,
            "Seoul": 8140, "Chicago": 9450, "Kuala Lumpur": 7410, "Beijing": 7050, "Zurich": 3160,
            "Vienna": 2500, "Barcelona": 3500, "Miami": 10520, "San Francisco": 12350, "Vancouver": 10380,
            "Munich": 2900, "Copenhagen": 3340, "Lisbon": 4300, "Stockholm": 3400, "Athens": 1280,
            "Dublin": 4050, "Prague": 2770, "Helsinki": 3380, "Abu Dhabi": 2100, "Doha": 1680,
            "Riyadh": 1400, "Warsaw": 2600, "Budapest": 2140, "Brussels": 3300, "Tel Aviv": 0
        }

        flight_distance = distance_map.get(flight.source, 0)
        flight_duration = (flight.landing_datetime - flight.departure_datetime).seconds // 60  # in minutes

        departure_congestion = random.randint(10, 50)
        arrival_congestion = random.randint(10, 50)
        departure_delay = random.choice([5, 10, 15, 20, 30])

        scheduled_departure = flight.departure_datetime + timedelta(minutes=30)
        actual_departure = scheduled_departure + timedelta(minutes=departure_delay)

        season = self.get_season(flight.landing_datetime)
        temperature = random.uniform(30, 45) if season == "Summer" else random.uniform(0, 15)

        weather_event = "Clear" if random.randint(0, 1) == 0 else "Adverse"

        flight_details = {
            'Season': season,
            'FlightDistance': flight_distance,
            'FlightDuration': flight_duration,
            'DepartureAirportCongestion': departure_congestion,
            'ArrivalAirportCongestion': arrival_congestion,
            'DayOfWeek': flight.landing_datetime.strftime('%A'),
            'TimeOfFlight': flight.departure_datetime.strftime('%H:%M'),
            'ScheduledDepartureTime': scheduled_departure.strftime('%H:%M'),
            'ActualDepartureTime': actual_departure.strftime('%H:%M'),
            'DepartureDelay': departure_delay,
            'Temperature': temperature,
            'Visibility': random.uniform(5, 10),
            'WindSpeed': random.uniform(5, 20),
            'WeatherEvent': weather_event
        }

        print("Sending flight details to prediction service:\n", flight_details)

        try:
            prediction_result = self.dal.Flight.is_landing_delayed(flight_details)
            print("Prediction result:\n", prediction_result)
            return prediction_result
        except Exception as e:
            print(f"Error predicting flight delay: {e}")
            raise FlightRetrievalException(f"Failed to retrieve flight delay status: {e}") from e

    def get_season(self, date):
        month = date.month
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"
        
    def show_error_message(self, message):
        QMessageBox.critical(None, "Error", message, QMessageBox.Ok)

    def show_success_message(self, message):
        QMessageBox.information(None, "Success", message, QMessageBox.Ok)

    def go_back(self):
        self.main_controller.go_back()