

from datetime import datetime
class FlightInfo:
    def __init__(self, flight_name):
        self.flight_name = flight_name
        #Here is all of the full details of flight

    def __repr__(self):
        return f"FlightInfo(flight_name={self.flight_name})"
    



class FlightInfoPartial:
    #Here is general information of any flight
    def __init__(self, id: int,date_and_time: datetime, source: str, destination: str):
        self.id = id
        self.date_and_time = date_and_time
        self.source = source
        self.destination = destination

    def save_to_db(self):
        pass

    def __repr__(self):
        return (f"FlightInfoPartial(id={self.id}, source_id={self.source_id}, longitude={self.longitude}, "
                f"latitude={self.latitude}, date_and_time={self.date_and_time}, source={self.source}, "
                f"destination={self.destination}, flight_code={self.flight_code})")
    
