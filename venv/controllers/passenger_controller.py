import pandas as pd
import requests
import random
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
from models.aircraft import Aircraft
from exceptions import TicketCreationException,TicketRetrievalException, FlightRetrievalException, AircraftNotFoundException, UnexpectedErrorException, NetworkException, FlightNotFoundException
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from PySide6.QtWidgets import QFileDialog
import os


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
                    print(f"Aircraft not found for flight {flight.id}")
            self.flights_view = FlightsView(controller=self, flights=future_flights)
            self.main_controller.set_view(self.flights_view)
        except FlightRetrievalException as fre:
            self.show_error_message(f"Unable to retrieve flights: {fre}")
        except NetworkException as ne:
            self.show_error_message(f"Network error while fetching flights: {ne}")
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
            tickets = self.dal.Ticket.get_user_tickets(self.current_user_id)
            self.my_flights_view = MyFlightsView(controller=self, tickets=tickets)
            self.main_controller.set_view(self.my_flights_view)
        except TicketRetrievalException as fre:
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

    def is_landing_delayed(self, flight):
        return 0
    
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

        # Randomize values based on your ranges
        departure_congestion = random.randint(10, 50)
        arrival_congestion = random.randint(10, 50)
        departure_delay = random.choice([5, 10, 15, 20, 30])

        # Set scheduled departure 30 minutes after time of flight
        scheduled_departure = flight.departure_datetime + timedelta(minutes=30)
        actual_departure = scheduled_departure + timedelta(minutes=departure_delay)

        # Random temperature logic based on a simple weather condition (e.g., hot/cold season)
        season = self.get_season(flight.landing_datetime)
        temperature = random.uniform(30, 45) if season == "Summer" else random.uniform(0, 15)

        weather_event = "Clear" if random.randint(0, 1) == 0 else "Adverse"

        # Create the prediction object
        new_landing_pred = pd.DataFrame({
            'Season': [season],
            'FlightDistance': [flight_distance],
            'FlightDuration': [flight_duration],
            'DepartureAirportCongestion': [departure_congestion],
            'ArrivalAirportCongestion': [arrival_congestion],
            'DayOfWeek': [flight.landing_datetime.strftime('%A')],
            'TimeOfFlight': [flight.departure_datetime.strftime('%H:%M')],
            'ScheduledDepartureTime': [scheduled_departure.strftime('%H:%M')],
            'ActualDepartureTime': [actual_departure.strftime('%H:%M')],
            'DepartureDelay': [departure_delay],
            'Temperature': [temperature],
            'Visibility': [random.uniform(5, 10)],
            'WindSpeed': [random.uniform(5, 20)],
            'WeatherEvent': [weather_event]
        })
        print ("new_landing_pred: \n",new_landing_pred)
        # Call the prediction function and return the result
        # return self.dal.Flight.is_landing_delayed(self, new_landing_pred)
        return self.is_landing_delayed(new_landing_pred)


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


    def download_ticket_pdf(self, ticket):
        # Open file dialog to select download location
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options
        )
        
        if not file_path:
            return  # User canceled the file dialog

        if not file_path.endswith(".pdf"):
            file_path += ".pdf"

        # Create the PDF document
        pdf = SimpleDocTemplate(file_path, pagesize=letter)

        # Define a list to hold the content of the PDF
        content = []

        # Set up the styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.fontSize = 20
        title_style.alignment = 1  # Center alignment
        
        normal_style = ParagraphStyle(
            name='Normal',
            fontSize=12,
            leading=14,
            alignment=1  # Centered text
        )

        label_style = ParagraphStyle(
            name='Label',
            fontSize=10,
            leading=12,
            textColor='gray',
            alignment=1  # Centered text
        )

        # Add the flight ticket icon
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'Flight_View', 'icons', 'ticket.png')
        if os.path.exists(icon_path):
            content.append(Image(icon_path, 1.5 * inch, 1.5 * inch))  # Ticket icon
        else:
            print(f"Error: Icon file not found at {icon_path}")

        # Flight Ticket Header (using Ticket ID)
        content.append(Paragraph(f"Flight Ticket: {ticket.id}", title_style))
        content.append(Spacer(1, 12))  # Add space below the title
        flight=self.dal.Flight.get_flight_by_id(ticket.flight_id)
        aircraft=self.dal.Aircraft.get_aircraft_by_id(flight.aircraft_id)
        # Displaying the ticket details (replacing flight ID with ticket details)
        details = [
            {"label": "Flight", "value": f"{flight.source} → {flight.destination}"},
            {"label": "Departure", "value": flight.departure_datetime.strftime('%Y-%m-%d %H:%M')},
            {"label": "Landing", "value": flight.landing_datetime.strftime('%Y-%m-%d %H:%M')},
            {"label": "Aircraft", "value": aircraft.nickname},
            {"label": "purchase time", "value": ticket.purchase_datetime.strftime('%Y-%m-%d %H:%M')}
        ]

        # Add the details in a ticket-like format
        for detail in details:
            content.append(Paragraph(detail["label"], label_style))
            content.append(Paragraph(detail["value"], normal_style))
            content.append(Spacer(1, 10))  # Space between details

        # Build the PDF
        pdf.build(content)

        # Notify user or perform post-generation actions
        print(f"PDF saved: {file_path}")
        os.startfile(file_path)  # This will open the file automatically on Windows

