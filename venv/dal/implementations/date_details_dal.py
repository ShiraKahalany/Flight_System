
from dal.interfaces.idal import IDateDetailsDAL
from models.hebrew_times import DateDetails
from datetime import datetime

class DateDetailsDAL(IDateDetailsDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    locations = {
        "New York": 5128581, "London": 2643743, "Tokyo": 1850147, "Paris": 2988507,
        "Los Angeles": 5368361, "Dubai": 292223, "Singapore": 1880252, "Hong Kong": 1819729,
        "Sydney": 2147714, "Toronto": 6167865, "Berlin": 2950159, "Amsterdam": 2759794,
        "Bangkok": 1609350, "Istanbul": 745044, "Moscow": 524901, "Mumbai": 1275339,
        "São Paulo": 3448439, "Mexico City": 3530597, "Johannesburg": 993800, "Cairo": 360630,
        "Delhi": 1261481, "Rome": 3169070, "Madrid": 3117735, "Frankfurt": 2925533,
        "Seoul": 1835848, "Chicago": 4887398, "Kuala Lumpur": 1735161, "Beijing": 1816670,
        "Zurich": 2657896, "Vienna": 2761369, "Barcelona": 3128760, "Miami": 4164138,
        "San Francisco": 5391959, "Vancouver": 6173331, "Munich": 2867714, "Copenhagen": 2618425,
        "Lisbon": 2267057, "Stockholm": 2673730, "Athens": 264371, "Dublin": 2964574,
        "Prague": 3067696, "Helsinki": 658225, "Abu Dhabi": 292968, "Doha": 290030,
        "Tel Aviv": 293397, "Riyadh": 108410, "Warsaw": 756135, "Budapest": 3054643,
        "Brussels": 2800866
    }

    def get_date_details(self, date: datetime, location: str) -> DateDetails:
        print(f'the date: {date} and location: {location}')
        date=date.strftime("%Y-%m-%dT%H:%M:%S")
        location_key = self.locations.get(location)
        res = self.api_client.post("times/checkdate", {"date": date, "location": location_key})
        return DateDetails.to_client_format(res.json())