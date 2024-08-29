from datetime import datetime
from Flight_BE.FlightInfo import FlightInfo,FlightInfoPartial

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.flights = {}  # Dictionary to hold <dateTime, flightInfo>

    def add_flight(self, flight_datetime, flight_info_part):
        if isinstance(flight_datetime, datetime) and isinstance(flight_info_part, FlightInfoPartial):
            self.flights[flight_datetime] = flight_info_part
        else:
            raise ValueError("Invalid types for flight_datetime or flight_info")

    def __repr__(self):
        return f"User(username={self.username}, flights={self.flights})"
