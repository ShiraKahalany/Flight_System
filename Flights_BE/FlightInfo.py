

from datetime import datetime
class FlightInfo:
    def __init__(self, flight_name, departure, destination):
        self.flight_name = flight_name
        self.departure = departure
        self.destination = destination

    def __repr__(self):
        return f"FlightInfo(flight_name={self.flight_name}, departure={self.departure}, destination={self.destination})"
    



class FlightInfoPartial:
    def __init__(self, id: int, source_id: str, longitude: float, latitude: float, 
                 date_and_time: datetime, source: str, destination: str, flight_code: str):
        self.id = id
        self.source_id = source_id
        self.longitude = longitude
        self.latitude = latitude
        self.date_and_time = date_and_time
        self.source = source
        self.destination = destination
        self.flight_code = flight_code

    def save_to_db(self):
        pass

    def __repr__(self):
        return (f"FlightInfoPartial(id={self.id}, source_id={self.source_id}, longitude={self.longitude}, "
                f"latitude={self.latitude}, date_and_time={self.date_and_time}, source={self.source}, "
                f"destination={self.destination}, flight_code={self.flight_code})")
