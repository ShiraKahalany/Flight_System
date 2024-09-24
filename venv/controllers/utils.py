from datetime import datetime
from dal.dal_factory import DALFactory
from models.hebrew_times import DateDetails
from models.flight import Flight

class Utils:
    def __init__(self):
        self.dal = DALFactory.get_instance()
    
    # def validate_aircraft_image(self, image_tags):
    #     valid_tags = ['airplane', 'aircraft', 'plane', 'jet']
    #     return any(tag.lower() in valid_tags for tag in image_tags)

    def check_aircraft_image(self, image_url: str) -> bool:
        return self.dal.ImageRecognition.is_aircraft_image(image_url)

    def get_date_info(self, date: datetime, location: str) -> DateDetails:
        return self.dal.DateDetails.get_date_details(date, location)
    
    def is_flight_during_shabbat_or_holiday(self, departure: datetime, arrival: datetime, location: str) -> bool:
        departure_info = self.get_date_info(departure, location)
        arrival_info = self.get_date_info(arrival, location)

        return (departure_info.day_of_week==6 or arrival_info.day_of_week==6 or
                departure_info.is_holiday or arrival_info.is_holiday)
    
    def is_flight_allowed(
            self, flight:Flight) -> bool:
        departure_info = self.get_date_info(flight.departure_datetime, flight.source)
        arrival_info = self.get_date_info(flight.landing_datetime, flight.destination)
        return (departure_info.day_of_week!=6 and arrival_info.day_of_week!=6 and
                not departure_info.is_holiday and not arrival_info.is_holiday)