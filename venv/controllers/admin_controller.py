from PySide6.QtWidgets import QMessageBox
from pydantic import ValidationError
from Flight_View.manager_view import ManagerView
from Flight_View.add_aircraft_view import AddAircraftView
from Flight_View.add_flight_view import AddFlightView  # New view for adding flights
from models.flight import Flight
from dal.interfaces.idal import IDAL
from datetime import datetime

class AdminController:
    def __init__(self, main_controller, dal: IDAL):
        self.main_controller = main_controller
        self.dal = dal

    def show_admin_view(self):
        # Recreate ManagerView each time it's needed
        self.manager_view = ManagerView(controller=self)
        self.main_controller.set_view(self.manager_view)  # Set the view in the main window

    def go_back(self):
        self.main_controller.go_back()  # Handle navigation

    def add_aircraft(self):
        """Show the AddAircraftView for adding a new aircraft."""
        self.add_aircraft_view = AddAircraftView(controller=self)
        self.main_controller.set_view(self.add_aircraft_view)

    def add_flight(self):
        """Show the AddFlightView for adding a new flight."""
        aircrafts = self.dal.Aircraft.getAircrafts()  # Fetch available aircrafts from DAL
        self.add_flight_view = AddFlightView(controller=self, aircrafts=aircrafts)
        self.main_controller.set_view(self.add_flight_view)

    def save_flight(self, aircraft_id, source, destination, departure_datetime, landing_datetime, price):
        """Save new flight data."""
        try:
            # Validate that departure and landing times are in the future
            if departure_datetime < datetime.now() or landing_datetime < datetime.now():
                raise ValueError("The departure and landing times must be in the future.")

            # Validate that landing time is after departure time
            if landing_datetime <= departure_datetime:
                raise ValueError("The landing time must be after the departure time.")

            # Create the new flight object
            new_flight = Flight(
                aircraft_id=aircraft_id,
                source=source,
                destination=destination,
                departure_datetime=departure_datetime,
                landing_datetime=landing_datetime,
                price=price
            )

            # Add the flight using the DAL
            new_flight_data = new_flight.to_server_format()
            created_flight = self.dal.Flight.create_flight(new_flight_data)

            print(f"New flight created: {created_flight}")

            # Show success message
            self.show_success_message(f"Flight added successfully!\n{created_flight}")

        except ValueError as ve:
            self.show_error_message(f"Error: {ve}")
        except Exception as e:
            self.show_error_message(f"Unexpected error: {e}")

    def show_success_message(self, message):
        """Show a pop-up success message."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Success")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.buttonClicked.connect(self.go_back)  # Go back to admin view when "OK" is clicked
        msg_box.exec()

    def show_error_message(self, message):
        """Show a pop-up error message."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()
