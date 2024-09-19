
from dal.interfaces.idal import IDateDetailsDAL
from models.hebrew_times import DateDetails
from datetime import datetime

class DateDetailsDAL(IDateDetailsDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_date_details(self, date: datetime, location: str) -> DateDetails:
        print(f'the date: {date} and location: {location}')
        date=date.strftime("%Y-%m-%dT%H:%M:%S")
        res=self.api_client.post("times/checkdate", {"date": date, "location": location})
        return DateDetails.to_client_format(res.json())