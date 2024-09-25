from PySide6.QtWidgets import QMessageBox
from pydantic import ValidationError
from Flight_View.manager_view import ManagerView
from Flight_View.add_aircraft_view import AddAircraftView
from Flight_View.add_flight_view import AddFlightView  # New view for adding flights
from models.flight import Flight
from dal.interfaces.idal import IDAL
from datetime import datetime
from models.aircraft import Aircraft
from exceptions import AircraftCreationException, AircraftRetrievalException, NetworkException, UnexpectedErrorException, FlightCreationException, ImageAnalysisException

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
        try:
            aircrafts = self.dal.Aircraft.get_aircrafts()
            self.add_flight_view = AddFlightView(controller=self, aircrafts=aircrafts)
            self.main_controller.set_view(self.add_flight_view)
        except AircraftRetrievalException:
            self.show_error_message("Failed to retrieve aircrafts. Please try again later.")
        except NetworkException:
            self.show_error_message("Network error occurred. Please check your internet connection and try again.")
        except Exception as e:
            self.show_error_message("An unexpected error occurred. Please try again later or contact support.")
            print(f"Unexpected error in add_flight: {e}")
    

    def validate_aircraft_input(self, manufacturer, nickname, year_of_manufacture, image_url, number_of_chairs):
        errors = []
        if not manufacturer or not nickname:
            errors.append("Manufacturer and nickname are required.")
        try:
            year = int(year_of_manufacture)
            if year > datetime.now().year:
                errors.append("Year of manufacture cannot be in the future.")
        except ValueError:
            errors.append("Year of manufacture must be a valid number.")
        if not image_url:
            errors.append("Image URL is required.")
        try:
            chairs = int(number_of_chairs)
            if chairs <= 0:
                errors.append("Number of chairs must be greater than zero.")
        except ValueError:
            errors.append("Number of chairs must be a valid number.")
        try:
            is_aircraft = self.dal.ImageRecognition.is_aircraft_image(image_url)
            if not is_aircraft:
                errors.append("The provided image does not appear to be an aircraft. Please upload an appropriate image.")
        except ImageAnalysisException:
            errors.append("Failed to analyze the image")
        except NetworkException:
            self.show_error_message("Network error occurred. Please check your internet connection and try again.")
        except Exception as e:
            self.show_error_message("An unexpected error occurred. Please try again later or contact support.")
        return errors

    def save_aircraft(self, manufacturer, nickname, year_of_manufacture, image_url, number_of_chairs):
        """Save new aircraft data."""
        errors = self.validate_aircraft_input(manufacturer, nickname, year_of_manufacture, image_url, number_of_chairs)
        if errors:
            self.show_error_message("\n".join(errors))
            return

        try:
            new_aircraft = Aircraft(
                manufacturer=manufacturer,
                nickname=nickname,
                year_of_manufacture=int(year_of_manufacture),
                image_url=image_url,
                number_of_chairs=int(number_of_chairs)
            )

            created_aircraft = self.dal.Aircraft.create_aircraft(new_aircraft)
            self.show_success_message(f"Aircraft added successfully!\n")

        except AircraftCreationException:
            self.show_error_message("Unable to create aircraft. There might be a problem with the server. Please try again later or contact support.")
        except NetworkException:
            self.show_error_message("Network error occurred. Please check your internet connection and try again.")
        except Exception as e:
            self.show_error_message("An unexpected error occurred. Please try again later or contact support.")
            print(f"Unexpected error in save_aircraft: {e}")



    def validate_flight_input(self, aircraft_id, source, destination, departure_datetime, landing_datetime, price):
        errors = []
        if not aircraft_id or not source or not destination or price=="":
            errors.append("All fields are required.")
        try:
            #dep_time = datetime.strptime(departure_datetime, "%Y-%m-%d %H:%M:%S")
            #land_time = datetime.strptime(landing_datetime, "%Y-%m-%d %H:%M:%S")
            if source == destination:
                errors.append("Departure and arrival locations cannot be the same.")
            if departure_datetime < datetime.now():
                errors.append("Departure time must be in the future.")
            if landing_datetime <= departure_datetime:
                errors.append("Landing time must be after departure time.")
        except ValueError:
            errors.append("Invalid date format. Use YYYY-MM-DD HH:MM:SS.")
        try:
            
            float_price = float(price)
            if float_price <= 0:
                errors.append("Price must be greater than zero.")
        except ValueError:
            errors.append("Price must be a valid number.")
            
        return errors

    def save_flight(self, aircraft_id, source, destination, departure_datetime, landing_datetime, price):
        """Save new flight data."""
        errors = self.validate_flight_input(aircraft_id, source, destination, departure_datetime, landing_datetime, price)
        if errors:
            self.show_error_message("\n".join(errors))
            return

        try:
            new_flight = Flight(
                aircraft_id=aircraft_id,
                source=source,
                destination=destination,
                departure_datetime=departure_datetime,
                landing_datetime=landing_datetime,
                price=float(price)
            )

            created_flight = self.dal.Flight.create_flight(new_flight)
            self.show_success_message(f"Flight from {source} to {destination} added successfully!")

        except FlightCreationException:
            self.show_error_message("Unable to create flight. There might be a problem with the server. Please try again later or contact support.")
        except NetworkException:
            self.show_error_message("Network error occurred. Please check your internet connection and try again.")
        except Exception as e:
            self.show_error_message("An unexpected error occurred. Please try again later or contact support.")
            print(f"Unexpected error in save_flight: {e}")


    def show_success_message(self, message):
        """Show a pop-up success message."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Success")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.buttonClicked.connect(self.go_back)
        msg_box.exec()

    def show_error_message(self, message):
        """Show a pop-up error message."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()