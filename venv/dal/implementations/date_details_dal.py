
from dal.interfaces.idal import IDateDetailsDAL
from models.hebrew_times import DateDetails
from datetime import datetime

class DateDetailsDAL(IDateDetailsDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_date_details(self, date: datetime, location: str) -> DateDetails:
        res=self.api_client.get("times/checkdate", {"date": date.isoformat(), "location": location})
        return DateDetails.to_client_format(res.json())