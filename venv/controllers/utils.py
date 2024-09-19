from datetime import datetime
from dal.dal_factory import DALFactory
from models.hebrew_times import ShabbatHolidayInfo
from models.hebrew_times import DateDetails

class Utils:
    def __init__(self):
        self.dal = DALFactory.get_instance()
    
    # def validate_aircraft_image(self, image_tags):
    #     valid_tags = ['airplane', 'aircraft', 'plane', 'jet']
    #     return any(tag.lower() in valid_tags for tag in image_tags)


    def get_date_info(self, date: datetime, location: str) -> DateDetails:
        return self.dal.DateDetails.get_date_details(date, location)
    
    
    def is_flight_during_shabbat_or_holiday(self, departure: datetime, arrival: datetime, location: str) -> bool:
        departure_info = self.get_date_info(departure, location)
        arrival_info = self.get_date_info(arrival, location)

        return (departure_info.is_shabbat or arrival_info.is_shabbat or
                departure_info.is_holiday or arrival_info.is_holiday)