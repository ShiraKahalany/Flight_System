import requests
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox
from Flight_View.passenger_view import PassengerView
from Flight_View.flights_view import FlightsView
from Flight_View.flight_entry_view import FlightEntryView
from Flight_View.landings_view import LandingsView  # Import the LandingsView
from Flight_View.mock_data import flights, tickets, aircrafts
from models.aircraft import Aircraft  # Ensure you import the Aircraft model
from datetime import datetime, timedelta
from models.ticket import Ticket
from Flight_View.my_flights_view import MyFlightsView

class PassengerController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.passenger_view = None
        self.current_user_id = None  # Set this when the user logs in

    def show_passenger_view(self):
        self.passenger_view = PassengerView(controller=self)
        self.main_controller.set_view(self.passenger_view)

    def go_back(self):
        self.main_controller.go_back()

    def book_flight(self, flight_id):
        try:
            flight = next((f for f in flights if f.id == flight_id), None)
            if not flight:
                raise ValueError("Flight not found")

            new_ticket = Ticket(
                id=len(tickets) + 1,
                flight_id=flight_id,
                user_id=self.current_user_id,
                purchase_datetime=datetime.now()
            )
            tickets.append(new_ticket)

            # Print the newly created ticket
            print(f"New Ticket Created: {new_ticket}")

            # Print the updated tickets list
            print("Updated Tickets List:")
            for ticket in tickets:
                print(ticket)

            # Show success message in a pop-up alert
            self.show_success_message("Flight booked successfully!")

        except ValueError as ve:
            self.passenger_view.show_error(str(ve))
        except Exception as e:
            self.passenger_view.show_error(f"Error booking flight: {str(e)}")

    def show_success_message(self, message):
        """Show a pop-up alert message"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Success")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def show_flights(self):
        self.flights_view = FlightsView(controller=self)
        self.main_controller.set_view(self.flights_view)

    def show_flight_details(self, flight_id):
        flight = next((f for f in flights if f.id == flight_id), None)
        if flight:
            self.flight_entry_view = FlightEntryView(controller=self, flight=flight)
            self.main_controller.set_view(self.flight_entry_view)

    def purchase_ticket(self, flight_id):
        """Calls the booking method to purchase a flight"""
        self.book_flight(flight_id)
        self.main_controller.go_back()  # After purchase, go back to the previous screen

    def watch_landings(self):
        """Show the LandingsView and pass the controller."""
        self.landings_view = LandingsView(controller=self)
        self.main_controller.set_view(self.landings_view)

    def get_upcoming_landings(self, hours_ahead):
        """Filter the landings happening within the next given hours."""
        now = datetime.now()
        future_time = now + timedelta(hours=hours_ahead)

        # Filter flights landing at Ben Gurion Airport within the time window
        filtered_flights = [f for f in flights if f.destination == "Ben Gurion Airport" and now <= f.landing_datetime <= future_time]
        return filtered_flights

    def get_aircraft_by_id(self, aircraft_id):
        """Retrieve aircraft by its ID."""
        aircraft = next((a for a in aircrafts if a.id == aircraft_id), None)
        return aircraft

    def download_image(self, url):
        """Download the image from the given URL and return its binary content."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses
            return response.content  # Return image data as bytes
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None

    def show_my_flights(self):
        """Shows the view of flights that the current user has booked."""
        self.my_flights_view = MyFlightsView(controller=self, user_id=self.current_user_id)
        self.main_controller.set_view(self.my_flights_view)
