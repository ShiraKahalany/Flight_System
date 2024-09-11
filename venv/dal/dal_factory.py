from dal.idal import IDAL
from dal.user_dal import UserDAL
from dal.flight_dal import FlightDAL
from dal.aircraft_dal import AircraftDAL
from dal.ticket_dal import TicketDAL


class DALFactory(IDAL):
    def __init__(self, api_client):
        self.user_dal = UserDAL(api_client)
        self.flight_dal = FlightDAL(api_client)
        self.aircraft_dal = AircraftDAL(api_client)
        self.ticket_dal = TicketDAL(api_client)

    def __getattr__(self, name):
        for dal in [self.user_dal, self.flight_dal, self.aircraft_dal, self.ticket_dal]:
            if hasattr(dal, name):
                return getattr(dal, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
