from datetime import datetime
from dal.dal_factory import DALFactory
from models.hebrew_times import ShabbatHolidayInfo

def validate_aircraft_image(image_tags):
    valid_tags = ['airplane', 'aircraft', 'plane', 'jet']
    return any(tag.lower() in valid_tags for tag in image_tags)

def is_shabbat(date, location):
    # Implementation of Shabbat checking logic
    # This should use an actual API or library for accurate results
    pass


class ShabbatHolidayService:
    def __init__(self):
        self.dal = DALFactory.get_instance()

    def get_info(self, date: datetime, location: str) -> ShabbatHolidayInfo:
        #call the application server via DAL
        data = self.dal.ShabbatHoliday.get_info(date, location)
        return ShabbatHolidayInfo(
            is_shabbat=data['is_shabbat'],
            is_holiday=data['is_holiday'],
            hebrew_date=data['hebrew_date'],
            gregorian_date=datetime.fromisoformat(data['gregorian_date']),
            parsha=data['parsha'],
            shabbat_start=datetime.fromisoformat(data['shabbat_start']),
            shabbat_end=datetime.fromisoformat(data['shabbat_end']),
            holiday_name=data.get('holiday_name'),
            holiday_start=datetime.fromisoformat(data['holiday_start']) if data.get('holiday_start') else None,
            holiday_end=datetime.fromisoformat(data['holiday_end']) if data.get('holiday_end') else None
        )

    def is_flight_during_shabbat_or_holiday(self, departure: datetime, arrival: datetime, location: str) -> bool:
        departure_info = self.get_info(departure, location)
        arrival_info = self.get_info(arrival, location)

        return (departure_info.is_shabbat or arrival_info.is_shabbat or
                departure_info.is_holiday or arrival_info.is_holiday)