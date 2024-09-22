from datetime import datetime
from typing import Optional

class Flight:
    def __init__(self, aircraft_id, source, destination, departure_datetime, landing_datetime, price, id=None, is_delay=None):
        self.id: Optional[int]=id
        self.aircraft_id = aircraft_id
        self.source = source
        self.destination = destination
        self.departure_datetime: datetime = departure_datetime
        self.landing_datetime: datetime = landing_datetime
        self.is_delay: Optional[bool] = is_delay
        self.price= price


    def to_server_format(self):

        def format_datetime(dt):
            return dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else None
        
        return {
            #"Id": self.id,
            "AircraftId": self.aircraft_id,
            "Source": self.source,
            "Destination": self.destination,
            "DepartureDatetime": format_datetime(self.departure_datetime),
            "LandingDatetime": format_datetime(self.landing_datetime),
            "IsDelay": self.is_delay if self.is_delay else None,
            "Price": self.price
        }

    @classmethod
    def to_client_format(cls, server_dict):

        def parse_datetime(dt_str):
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S") if dt_str else None
        return cls(
            id=int(server_dict["id"]),
            aircraft_id=int(server_dict["aircraftId"]),
            source=server_dict["source"],
            destination=server_dict["destination"],
            departure_datetime=parse_datetime(server_dict["departureDatetime"]),
            landing_datetime=parse_datetime(server_dict["landingDatetime"]),
            is_delay=server_dict["isDelay"] if server_dict["isDelay"] else None,
            price=server_dict["price"]
        )