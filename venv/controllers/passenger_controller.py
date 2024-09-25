from Flight_View.passenger_view import PassengerView
from Flight_View.flights_view import FlightsView
from Flight_View.flight_entry_view import FlightEntryView
from Flight_View.landings_view import LandingsView
from Flight_View.my_flights_view import MyFlightsView
from PySide6.QtWidgets import QMessageBox


class PassengerController:
    def __init__(self, main_controller, dal, flight_booking_controller, my_flights_controller, landings_controller):
        self.main_controller = main_controller
        self.my_flights_controller = my_flights_controller
        self.flight_booking_controller = flight_booking_controller
        self.landings_controller = landings_controller
        self.dal = dal
        self.passenger_view = None
        self.current_user_id = None

    def show_passenger_view(self, user=None, date_details=None):
        self.passenger_view = PassengerView(controller=self, user=user, date_details=date_details)
        self.main_controller.set_view(self.passenger_view)

    def go_back(self):
        self.main_controller.go_back()

    def show_flights(self):
        self.flight_booking_controller.show_flights()

    def show_my_flights(self):
        self.my_flights_controller.show_my_flights(self.current_user_id)

    def watch_landings(self):
        self.landings_controller.watch_landings()

    def show_error_message(self, message):
        QMessageBox.critical(None, "Error", message, QMessageBox.Ok)

    def show_success_message(self, message):
        QMessageBox.information(None, "Success", message, QMessageBox.Ok)