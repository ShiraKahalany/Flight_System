from PySide6.QtWidgets import QMessageBox
from pydantic import ValidationError
import requests
from Flight_View.manager_view import ManagerView
from Flight_View.add_aircraft_view import AddAircraftView
from Flight_View.add_flight_view import AddFlightView  # New view for adding flights
from Flight_View.manager_flights_view import ManagerFlightsView
from Flight_View.purchase_summary_view import PurchaseSummaryView
from models.flight import Flight
from dal.interfaces.idal import IDAL
from datetime import datetime
from models.aircraft import Aircraft
from exceptions import FlightRetrievalException,AircraftNotFoundException, AircraftCreationException, AircraftRetrievalException, NetworkException, UnexpectedErrorException, FlightCreationException, ImageAnalysisException
from collections import defaultdict
from datetime import timedelta
from PySide6.QtCore import Qt
from dateutil.relativedelta import relativedelta
from collections import defaultdict

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


    def show_all_flights(self):
        """Fetch and display all upcoming flights for the manager."""
        try:
            all_flights = self.dal.Flight.get_flights()  # Retrieve flights from DAL
            for flight in all_flights:
                try:
                    aircraft = self.dal.Aircraft.get_aircraft_by_id(flight.aircraft_id)
                    flight.aircraft = aircraft
                    if aircraft and aircraft.image_url:
                        aircraft.image_data = self.download_image(aircraft.image_url)
                except AircraftNotFoundException:
                    flight.aircraft = None
                    print(f"Aircraft not found for flight {flight.id}")
            
            self.manager_flights_view = ManagerFlightsView(controller=self, flights=all_flights)
            self.main_controller.set_view(self.manager_flights_view)
        except FlightRetrievalException as fre:
            self.show_error_message(f"Unable to retrieve flights: {fre}")
        except NetworkException as ne:
            self.show_error_message(f"Network error while fetching flights: {ne}")
        except UnexpectedErrorException as uee:
            self.show_error_message("An unexpected error occurred. Please try again later.")
            print(f"Unexpected error in show_all_flights: {uee}")
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
        
    def show_purchase_summary(self):
        """Show the purchase summary view with a graph for the next 12 months, based on flight departure dates."""
        try:
            # Fetch all flights
            all_flights = self.dal.Flight.get_flights()

            # Fetch all tickets
            all_tickets = self.dal.Ticket.get_tickets()

            # Process the tickets by the month of the flight's departure date
            current_date = datetime.now()

            # Get the months from this month (inclusive) to the next 12 months
            next_12_months = [(current_date + relativedelta(months=i)).strftime('%Y-%m') for i in range(12)]
            tickets_by_month = defaultdict(int)

            # Create a mapping of flight ID to departure month
            flight_departure_month = {}
            for flight in all_flights:
                departure_month = flight.departure_datetime.strftime('%Y-%m')
                if departure_month in next_12_months:
                    flight_departure_month[flight.id] = departure_month

            # Count tickets for flights with departures in the next 12 months
            for ticket in all_tickets:
                flight_id = ticket.flight_id
                if flight_id in flight_departure_month:
                    departure_month = flight_departure_month[flight_id]
                    tickets_by_month[departure_month] += 1

            # Sort the ticket purchases by the next 12 months
            sorted_purchases = [tickets_by_month[month] for month in next_12_months]

            # Create the PurchaseSummaryView and plot the data
            self.purchase_summary_view = PurchaseSummaryView(controller=self)
            self.purchase_summary_view.plot_graph([month.split('-')[1] for month in next_12_months], sorted_purchases)  # Show only month numbers on the X-axis
            self.main_controller.set_view(self.purchase_summary_view)

        except Exception as e:
            self.show_error_message(f"Error loading purchase summary: {e}")

