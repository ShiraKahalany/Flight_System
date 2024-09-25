from controllers.login_controller import LoginController
from controllers.admin_controller import AdminController
from controllers.passenger_controller import PassengerController
from controllers.flight_booking_controller import FlightBookingController
from controllers.my_flights_controller import MyFlightsController
from controllers.landings_controller import LandingsController
from dal.interfaces.idal import IDAL

class MainController:
    def __init__(self, dal: IDAL):
        self.dal = dal
        self.main_window = None
        self.admin_controller = AdminController(self, dal)
        #self.passenger_controller = PassengerController(self, dal)
        
        # Create sub-controllers for passenger functionality
        flight_booking_controller = FlightBookingController(self, dal)
        my_flights_controller = MyFlightsController(self, dal)
        landings_controller = LandingsController(self, dal)
        
        self.passenger_controller = PassengerController(
            self,
            dal,
            flight_booking_controller,
            my_flights_controller,
            landings_controller
        )

        # Pass both admin_controller and passenger_controller to LoginController
        self.login_controller = LoginController(self, self.admin_controller, self.passenger_controller)

    def show_main_window(self):
        # self.main_window = MainWindow(self)
        self.main_window.show()

    def show_login(self):
        self.login_controller.show_login()

