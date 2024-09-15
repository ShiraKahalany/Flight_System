#from views.admin_view import AdminView
from dal.interfaces.idal import IDAL
from utils import validate_aircraft_image

class AdminController:
    def __init__(self, main_controller, dal: IDAL):
        self.main_controller = main_controller
        self.dal = dal
        self.admin_view = None

    def show_admin_view(self):
        #self.admin_view = AdminView(self)
        self.admin_view.show()

    def add_aircraft(self, manufacturer, nickname, year_of_manufacture, image_url):
        try:
            image_tags = self.dal.Aircraft.get_image_tags(image_url)
            
            if not validate_aircraft_image(image_tags):
                raise ValueError("The image does not appear to be an aircraft")

            aircraft_data = {
                "manufacturer": manufacturer,
                "nickname": nickname,
                "year_of_manufacture": year_of_manufacture,
                "image_url": image_url
            }
            aircraft = self.dal.Aircraft.create_aircraft(aircraft_data)
            self.admin_view.update_aircraft_list(aircraft)
            self.admin_view.show_success("Aircraft added successfully")
        except ValueError as ve:
            self.admin_view.show_error(str(ve))
        except Exception as e:
            self.admin_view.show_error(f"Error adding aircraft: {str(e)}")

    def add_flight(self, aircraft_id, source, destination, departure_datetime, landing_datetime):
        try:
            flight_data = {
                "aircraft_id": aircraft_id,
                "source": source,
                "destination": destination,
                "departure_datetime": departure_datetime,
                "landing_datetime": landing_datetime
            }
            flight = self.dal.Flight.create_flight(flight_data)
            self.admin_view.update_flight_list(flight)
            self.admin_view.show_success("Flight added successfully")
        except Exception as e:
            self.admin_view.show_error(f"Error adding flight: {str(e)}")