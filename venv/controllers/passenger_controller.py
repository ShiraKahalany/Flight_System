from PySide6.QtWidgets import QMessageBox
#from views.passenger_view import PassengerView
from models.ticket import Ticket
from dal.idal import IDAL

class PassengerController:
    def __init__(self, main_controller, dal: IDAL):
        self.main_controller = main_controller
        self.dal = dal
        self.passenger_view = None
        self.current_user_id = None  # Set this when user logs in

    def show_passenger_view(self):
        #self.passenger_view = PassengerView(self)
        self.passenger_view.show()

    # def book_flight(self, flight_id):
    #     try:
    #         ticket_data = {
    #             "flight_id": flight_id,
    #             "user_id": self.current_user_id
    #         }
    #         ticket = self.dal.create_ticket(ticket_data)
    #         self.passenger_view.update_booked_flights(ticket)
    #     except Exception as e:
    #         self.passenger_view.show_error(str(e))

    def book_flight(self, flight_id):
        try:
            flight = self.dal.get_flight(flight_id)
            if is_shabbat(flight.landing_datetime, flight.destination):
                raise ValueError("This flight lands during Shabbat")
        
            ticket_data = {
              "flight_id": flight_id,
                "user_id": self.current_user_id
            }
            ticket = self.dal.create_ticket(ticket_data)
            self.passenger_view.update_booked_flights(ticket)
        except Exception as e:
            self.passenger_view.show_error(str(e))


    def get_upcoming_landings(self, hours_ahead):
        try:
            flights = self.dal.get_upcoming_landings(hours_ahead)
            self.passenger_view.display_upcoming_landings(flights)
        except Exception as e:
            self.passenger_view.show_error(str(e))

    def get_user_flights(self):
        try:
            flights = self.dal.get_user_flights(self.current_user_id)
            self.passenger_view.display_user_flights(flights)
        except Exception as e:
            self.passenger_view.show_error(str(e))

    def get_user_tickets(self):
        try:
            tickets = self.dal.get_user_tickets(self.current_user_id)
            self.passenger_view.display_user_tickets(tickets)
        except Exception as e:
            self.passenger_view.show_error(str(e))