from datetime import datetime
from typing import Optional

class Flight:
    def __init__(self, aircraft_id, source, destination, departure_datetime, landing_datetime, price=0, id=None, is_delay=False):
        if price < 0:
            raise ValueError("Price cannot be negative")
        
        self.id: Optional[int] = id
        self.aircraft_id = aircraft_id
        self.source = source
        self.destination = destination
        self.departure_datetime: datetime = departure_datetime
        self.landing_datetime: datetime = landing_datetime
        self.is_delay: bool= is_delay
        self.price = price  # Default to 0 if price is not provided

    def to_server_format(self):
        return {
            "AircraftId": self.aircraft_id,
            "Source": self.source,
            "Destination": self.destination,
            "DepartureDatetime": self.departure_datetime.strftime("%Y-%m-%dT%H:%M:%S") if self.departure_datetime else None,
            "LandingDatetime": self.landing_datetime.strftime("%Y-%m-%dT%H:%M:%S") if self.landing_datetime else None,
            "IsDelay": self.is_delay,
            "Price": self.price
        }

    @classmethod
    def to_client_format(cls, server_dict: dict) -> 'Flight':
        def parse_datetime(dt_str):
            return datetime.strptime(dt_str.split('.')[0], "%Y-%m-%dT%H:%M:%S") if dt_str else None

        return cls(
            id=int(server_dict["id"]),
            aircraft_id=int(server_dict["aircraftId"]),
            source=server_dict["source"],
            destination=server_dict["destination"],
            departure_datetime=parse_datetime(server_dict["departureDatetime"]),
            landing_datetime=parse_datetime(server_dict["landingDatetime"]),
            is_delay=server_dict.get("isDelay", False),
            price=server_dict.get("price", 0)  # Default to 0 if price is missing
        )

    # print all the data of the flight
    def __str__(self):
        return f"Flight {self.id}: {self.source} to {self.destination} on {self.departure_datetime} price {self.price} is_delay {self.is_delay} aircraft_id {self.aircraft_id}"
