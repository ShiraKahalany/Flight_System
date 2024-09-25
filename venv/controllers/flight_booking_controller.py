from PySide6.QtWidgets import QMessageBox
from Flight_View.flights_view import FlightsView
from Flight_View.flight_entry_view import FlightEntryView
from models.ticket import Ticket
from exceptions import TicketCreationException, NetworkException, UnexpectedErrorException, AircraftNotFoundException
from datetime import datetime
import requests

class FlightBookingController:
    def __init__(self, main_controller, dal):
        self.main_controller = main_controller
        self.dal = dal
        self.current_user_id = None

    def show_flights(self):
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
            flights_view = FlightsView(controller=self, flights=future_flights)
            self.main_controller.set_view(flights_view)
        except Exception as e:
            self.show_error_message(f"Error loading flights: {e}")

    def show_flight_details(self, flight_id):
        try:
            flight = self.dal.Flight.get_flight_by_id(flight_id)
            if flight:
                flight.aircraft = self.dal.Aircraft.get_aircraft_by_id(flight.aircraft_id)
                flight_entry_view = FlightEntryView(controller=self, flight=flight)
                self.main_controller.set_view(flight_entry_view)
            else:
                raise Exception("Flight not found")
        except Exception as e:
            self.show_error_message(f"Error loading flight details: {e}")

    def book_flight(self, flight_id, user_id):
        try:
            if self.is_flight_during_shabbat_or_holiday(flight_id):
                self.show_error_message("The flight is during Shabbat or a holiday, \n it is not possible to buy a ticket.")
                return
            
            new_ticket = Ticket(
                flight_id=flight_id,
                user_id=user_id,
                purchase_datetime=datetime.now()
            )
            self.dal.Ticket.create_ticket(new_ticket)
            self.show_success_message("Flight booked successfully!")
        except Exception as e:
            self.show_error_message(f"Error booking flight: {e}")
            
    def purchase_ticket(self, flight_id):
        """Calls the booking method to purchase a flight."""
        self.book_flight(flight_id, self.current_user_id)
        self.main_controller.go_back()


    def is_flight_during_shabbat_or_holiday(self, flight_id):
        try:
            flight = self.dal.Flight.get_flight_by_id(flight_id)
            departure_info = self.dal.DateDetails.get_date_details(flight.departure_datetime, flight.source)
            arrival_info = self.dal.DateDetails.get_date_details(flight.landing_datetime, flight.destination)
            return (departure_info.day_of_week == 6 or arrival_info.day_of_week == 6 or
                    departure_info.is_holiday or arrival_info.is_holiday)
        except Exception as e:
            self.show_error_message(f"Error checking flight schedule: {e}")
            return False

    def download_image(self, url):
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
        
    def set_current_user(self, user_id):
        self.current_user_id = user_id
        
    def go_back(self):
        self.main_controller.go_back()

    def show_error_message(self, message):
        QMessageBox.critical(None, "Error", message, QMessageBox.Ok)

    def show_success_message(self, message):
        QMessageBox.information(None, "Success", message, QMessageBox.Ok)