
from dal.interfaces.idal import IDateDetailsDAL
from models.hebrew_times import DateDetails
from datetime import datetime

class DateDetailsDAL(IDateDetailsDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_date_details(self, date: datetime, location: str) -> DateDetails:
        response = self.api_client.get(
            "date_type_info",
            params={"date": date.isoformat(), "location": location}
        )
        return DateDetails(
            gregorian_date=datetime.fromisoformat(response['gregorian_date']),
            hebrew_date=response['hebrew_date'],
            day_of_week=response['day_of_week'],
            is_holiday=response['is_holiday'],
            parasha=response.get('parasha'),
            holiday_name=response.get('holiday_name'),
            shabbat_start=datetime.fromisoformat(response['shabbat_start']),
            shabbat_end=datetime.fromisoformat(response['shabbat_end']),
            holiday_start=datetime.fromisoformat(response['holiday_start']) if response.get('holiday_start') else None,
            holiday_end=datetime.fromisoformat(response['holiday_end']) if response.get('holiday_end') else None
        )