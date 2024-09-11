from PySide6.QtWidgets import QMessageBox
#from views.admin_view import AdminView
from models.aircraft import Aircraft
from datetime import datetime
from dal.idal import IDAL

class AdminController:
    def __init__(self, main_controller, dal: IDAL):
        self.main_controller = main_controller
        self.dal = dal
        self.admin_view = None

    def show_admin_view(self):
        #self.admin_view = AdminView(self)
        self.admin_view.show()

    # def add_aircraft(self, manufacturer, nickname, year_of_manufacture, image_url):
    #     try:
    #         aircraft_data = {
    #             "manufacturer": manufacturer,
    #             "nickname": nickname,
    #             "year_of_manufacture": year_of_manufacture,
    #             "image_url": image_url
    #         }
    #         aircraft = self.dal.create_aircraft(aircraft_data)
    #         self.admin_view.update_aircraft_list(aircraft)
    #     except Exception as e:
    #         self.admin_view.show_error(str(e))

    def add_flight(self, aircraft_id, source, destination, departure_datetime, landing_datetime):
        try:
            flight_data = {
                "aircraft_id": aircraft_id,
                "source": source,
                "destination": destination,
                "departure_datetime": departure_datetime.isoformat(),
                "landing_datetime": landing_datetime.isoformat()
            }
            flight = self.dal.create_flight(flight_data)
            self.admin_view.update_flight_list(flight)
        except Exception as e:
            self.admin_view.show_error(str(e))


    def add_aircraft(self, manufacturer, nickname, year_of_manufacture, image_url):
        try:
            image_tags = self.dal.get_image_tags(image_url)
            if not validate_aircraft_image(image_tags):
                raise ValueError("The image does not appear to be an aircraft")
            aircraft_data = {
                "manufacturer": manufacturer,
                "nickname": nickname,
                "year_of_manufacture": year_of_manufacture,
                "image_url": image_url
            }
            aircraft = self.dal.create_aircraft(aircraft_data)
            self.admin_view.update_aircraft_list(aircraft)
        except Exception as e:
            self.admin_view.show_error(str(e))

def validate_aircraft_image(image_tags):
    valid_tags = ['plane', 'flight', 'aircraft', 'airplane', 'jet']
    return any(tag.lower() in valid_tags for tag in image_tags.split(','))
