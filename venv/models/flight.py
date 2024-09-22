from datetime import datetime
from typing import Optional

class Flight:
    def __init__(self, aircraft_id, source, destination, departure_datetime, landing_datetime, price=0, id=None, is_delay=None):
        self.id: Optional[int] = id
        self.aircraft_id = aircraft_id
        self.source = source
        self.destination = destination
        self.departure_datetime: datetime = departure_datetime
        self.landing_datetime: datetime = landing_datetime
        self.is_delay: Optional[bool] = is_delay
        self.price = price  # Default to 0 if price is not provided

    def to_server_format(self):
        def format_datetime(dt):
            return dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else None

        return {
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
            return datetime.strptime(dt_str.split('.')[0], "%Y-%m-%dT%H:%M:%S") if dt_str else None

        # Default price to 0 if it's not present in the server_dict
        return cls(
            id=int(server_dict["id"]),
            aircraft_id=int(server_dict["aircraftId"]),
            source=server_dict["source"],
            destination=server_dict["destination"],
            departure_datetime=parse_datetime(server_dict["departureDatetime"]),
            landing_datetime=parse_datetime(server_dict["landingDatetime"]),
            is_delay=server_dict.get("isDelay"),
            price=server_dict.get("price", 0)  # Default to 0 if price is missing
        )

    # print all the data of the flight
    def __str__(self):
        return f"Flight {self.id}: {self.source} to {self.destination} on {self.departure_datetime} price {self.price} is_delay {self.is_delay} aircraft_id {self.aircraft_id}" 
