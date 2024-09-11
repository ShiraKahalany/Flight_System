from dal.interfaces.idal import IDAL
from dal.implementations.user_dal import UserDAL
from dal.implementations.flight_dal import FlightDAL
from dal.implementations.aircraft_dal import AircraftDAL
from dal.implementations.ticket_dal import TicketDAL
from dal.api_client import APIClient

class DALImpl(IDAL):
    def __init__(self):
        api_client = APIClient()
        self._user = UserDAL(api_client)
        self._flight = FlightDAL(api_client)
        self._aircraft = AircraftDAL(api_client)
        self._ticket = TicketDAL(api_client)

    @property
    def User(self) -> UserDAL:
        return self._user

    @property
    def Flight(self) -> FlightDAL:
        return self._flight

    @property
    def Aircraft(self) -> AircraftDAL:
        return self._aircraft

    @property
    def Ticket(self) -> TicketDAL:
        return self._ticket