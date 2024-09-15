from Flight_View.passenger_view import PassengerView
from Flight_View.mock_data import flights, tickets
from datetime import datetime, timedelta
from controllers.utils import is_shabbat

class PassengerController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.passenger_view = None
        self.current_user_id = None  # Set this when user logs in

    def show_passenger_view(self):
        # Recreate PassengerView each time it's needed
        self.passenger_view = PassengerView(controller=self)
        self.main_controller.set_view(self.passenger_view)  # Set the view in the main window

    def go_back(self):
        # Delegate the navigation back to the main controller
        self.main_controller.go_back()

    def book_flight(self, flight_id):
        try:
            flight = next((f for f in flights if f['id'] == flight_id), None)
            if not flight:
                raise ValueError("Flight not found")
            if is_shabbat(flight['landing_datetime'], flight['destination']):
                raise ValueError("This flight lands during Shabbat")

            new_ticket = {
                'id': len(tickets) + 1,
                'flight_id': flight_id,
                'user_id': self.current_user_id,
                'purchase_datetime': datetime.now()
            }
            tickets.append(new_ticket)
            self.passenger_view.update_booked_flights(new_ticket)
            self.passenger_view.show_success("Flight booked successfully")
        except ValueError as ve:
            self.passenger_view.show_error(str(ve))
        except Exception as e:
            self.passenger_view.show_error(f"Error booking flight: {str(e)}")

    def get_upcoming_landings(self, hours_ahead):
        try:
            now = datetime.now()
            upcoming_flights = [f for f in flights if now <= f['landing_datetime'] <= now + timedelta(hours=hours_ahead)]
            self.passenger_view.display_upcoming_landings(upcoming_flights)
        except Exception as e:
            self.passenger_view.show_error(f"Error retrieving upcoming landings: {str(e)}")


    def show_flights(self):
        pass

    def watch_landings(self):
        pass

    def show_my_flights(self):
        pass