from datetime import datetime

class Flight:
    def __init__(self, id, aircraft_id, source, destination, departure_datetime, landing_datetime):
        self.id = id
        self.aircraft_id = aircraft_id
        self.source = source
        self.destination = destination
        self.departure_datetime = departure_datetime
        self.landing_datetime = landing_datetime