import pandas as pd
import requests
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox
from Flight_View.passenger_view import PassengerView
from Flight_View.flights_view import FlightsView
from Flight_View.flight_entry_view import FlightEntryView
from Flight_View.landings_view import LandingsView
from models.ticket import Ticket
from Flight_View.my_flights_view import MyFlightsView
from dal.interfaces.idal import IDAL
from datetime import datetime, timedelta
from controllers.utils import Utils
from models.aircraft import Aircraft
from exceptions import TicketCreationException , FlightRetrievalException, AircraftNotFoundException, UnexpectedErrorException, NetworkException, FlightNotFoundException
class PassengerController:
    def __init__(self, main_controller, dal: IDAL):
        self.main_controller = main_controller
        self.dal = dal
        self.passenger_view = None
        self.current_user_id = None  # Set this when the user logs in

    def show_passenger_view(self):
        self.passenger_view = PassengerView(controller=self)
        self.main_controller.set_view(self.passenger_view)

    def go_back(self):
        self.main_controller.go_back()

    def book_flight(self, flight_id):
        """Functionality to book a flight."""
        try:
            new_ticket = Ticket(
                flight_id=flight_id,
                user_id=self.current_user_id,
                purchase_datetime=datetime.now()
            )
            if not Utils.is_flight_allowed(flight_id):
                self.show_error_message("The flight is during Shabbat or a holiday, \n it is not possible to buy a ticket.")
                print
                return
            self.dal.Ticket.create_ticket(new_ticket)
            print(f"New Ticket Created: {new_ticket}")
            self.show_success_message("Flight booked successfully!")
        except TicketCreationException as tce:
            self.show_error_message(f"Unable to book the flight: {tce}")
        except NetworkException as ne:
            self.show_error_message(f"Network error while booking flight: {ne}")
        except UnexpectedErrorException as uee:
            self.show_error_message("An unexpected error occurred. Please try again later.")
            print(f"Unexpected error in book_flight: {uee}")
        except Exception as e:
            self.show_error_message("An error occurred while booking the flight. Please try again.")
            print(f"Unhandled exception in book_flight: {e}")

    def show_flights(self):
        """Fetch and show all available future flights."""
        try:
            future_flights = self.dal.Flight.get_flights()
            for flight in future_flights:
                try:
                    aircraft = self.dal.Aircraft.get_aircraft_by_id(flight.aircraft_id)
                    flight.aircraft = aircraft
                    if aircraft and aircraft.image_url:
                        aircraft.image_data = self.download_image(aircraft.image_url)
                except AircraftNotFoundException:
                    flight.aircraft = None
                    print(f"Error loading the flights, sorry")
            self.flights_view = FlightsView(controller=self, flights=future_flights)
            self.main_controller.set_view(self.flights_view)
        except FlightRetrievalException as fre:
            self.show_error_message(f"Unable to retrieve flights")
        except NetworkException as ne:
            self.show_error_message(f"Network error while fetching flights")
        except UnexpectedErrorException as uee:
            self.show_error_message("An unexpected error occurred. Please try again later.")
            print(f"Unexpected error in show_flights: {uee}")
        except Exception as e:
            self.show_error_message(f"Error loading flights: {e}")



    def download_image(self, url):
        """Download the image from the given URL and return its binary content."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")
            return None

    def show_flight_details(self, flight_id):
        """Shows the details of the selected flight."""
        try:
            flight = self.dal.Flight.get_flight_by_id(flight_id)
            if flight:
                flight.aircraft = self.dal.Aircraft.get_aircraft_by_id(flight.aircraft_id)
                self.flight_entry_view = FlightEntryView(controller=self, flight=flight)
                self.main_controller.set_view(self.flight_entry_view)
            else:
                raise FlightNotFoundException(f"Flight with id {flight_id} not found")
        except FlightNotFoundException as fnf:
            self.show_error_message(f"Flight not found: {fnf}")
        except AircraftNotFoundException as anf:
            self.show_error_message(f"Aircraft information not available for this flight: {anf}")
        except NetworkException as ne:
            self.show_error_message(f"Network error while fetching flight details: {ne}")
        except UnexpectedErrorException as uee:
            self.show_error_message("An unexpected error occurred. Please try again later.")
            print(f"Unexpected error in show_flight_details: {uee}")
        except Exception as e:
            self.show_error_message("An error occurred while loading flight details. Please try again.")
            print(f"Unhandled exception in show_flight_details: {e}")

    def purchase_ticket(self, flight_id):
        """Calls the booking method to purchase a flight."""
        self.book_flight(flight_id)
        self.main_controller.go_back()

    def watch_landings(self):
        """Fetch and show landings in Ben Gurion Airport within the next 5 hours."""
        try:
            flights_in_next_5_hours = self.dal.Flight.get_BGR_lands_next_5_hours()
            self.landings_view = LandingsView(controller=self)
            self.main_controller.set_view(self.landings_view)
        except FlightRetrievalException as fre:
            self.show_error_message(f"Unable to retrieve landing information: {fre}")
        except NetworkException as ne:
            self.show_error_message(f"Network error while fetching landings: {ne}")
        except UnexpectedErrorException as uee:
            self.show_error_message("An unexpected error occurred. Please try again later.")
            print(f"Unexpected error in watch_landings: {uee}")
        except Exception as e:
            self.show_error_message("An error occurred while fetching landings. Please try again.")
            print(f"Unhandled exception in watch_landings: {e}")

    def get_upcoming_landings(self, hours_ahead):
        """Filter the landings happening within the next given hours."""
        try:
            flights_in_next_5_hours = self.dal.Flight.get_BGR_lands_next_5_hours()
            now = datetime.now()
            future_time = now + timedelta(hours=hours_ahead)
            filtered_flights = [f for f in flights_in_next_5_hours if now <= f.landing_datetime <= future_time]
            return filtered_flights
        except FlightRetrievalException as fre:
            self.show_error_message(f"Unable to retrieve upcoming landings: {fre}")
        except Exception as e:
            self.show_error_message("An error occurred while fetching upcoming landings.")
            print(f"Error in get_upcoming_landings: {e}")
        return []

    def show_my_flights(self):
        """Shows the view of flights that the current user has booked."""
        try:
            flights = self.dal.Flight.get_flights_of_user(self.current_user_id)
            self.my_flights_view = MyFlightsView(controller=self, flights=flights)
            self.main_controller.set_view(self.my_flights_view)
        except FlightRetrievalException as fre:
            self.show_error_message(f"Unable to retrieve your flights: {fre}")
        except NetworkException as ne:
            self.show_error_message(f"Network error while fetching your flights: {ne}")
        except UnexpectedErrorException as uee:
            self.show_error_message("An unexpected error occurred. Please try again later.")
            print(f"Unexpected error in show_my_flights: {uee}")
        except Exception as e:
            self.show_error_message("An error occurred while loading your flights. Please try again.")
            print(f"Unhandled exception in show_my_flights: {e}")

    def show_success_message(self, message):
        """Show a pop-up alert message."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Success")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def predict_landing_delay(self, flight):
        """Predict if the landing will be delayed for a given flight."""
        
        # Sample distances for common destinations
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

        # Create the prediction object
        new_landing_pred = pd.DataFrame({
            'Season': [self.get_season(flight.landing_datetime)],
            'FlightDistance': [flight_distance],
            'FlightDuration': [flight_duration],
            'DepartureAirportCongestion': [30],  # Randomly setting it to 30 for this example
            'ArrivalAirportCongestion': [40],  # Randomly setting it to 40 for this example
            'DayOfWeek': [flight.landing_datetime.strftime('%A')],
            'TimeOfFlight': [flight.departure_datetime.strftime('%H:%M')],
            'ScheduledDepartureTime': ['07:30'],  # A placeholder, can be derived more dynamically
            'ActualDepartureTime': ['07:45'],  # Can be calculated based on delay
            'DepartureDelay': [15],  # Example delay
            'Temperature': [18.5],  # Example temperature
            'Visibility': [10],  # Example visibility
            'WindSpeed': [12.3],  # Example wind speed
            'WeatherEvent': ['Clear']  # Example weather event
        })

        # Call the prediction function and return the result
        return self.dal.Flight.is_landing_delayed(new_landing_pred)

    def get_season(self, date):
        """Determine the season from the date."""
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
        """Show a pop-up error message."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()