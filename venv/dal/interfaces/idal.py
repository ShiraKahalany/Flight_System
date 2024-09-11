from abc import ABC, abstractmethod
from dal.interfaces.iuser_dal import IUserDAL
from dal.interfaces.iflight_dal import IFlightDAL
from dal.interfaces.iaircraft_dal import IAircraftDAL
from dal.interfaces.iticket_dal import ITicketDAL

class IDAL(ABC):
    @property
    @abstractmethod
    def User(self) -> IUserDAL:
        pass

    @property
    @abstractmethod
    def Flight(self) -> IFlightDAL:
        pass

    @property
    @abstractmethod
    def Aircraft(self) -> IAircraftDAL:
        pass


    @property
    @abstractmethod
    def Ticket(self) -> ITicketDAL:
        pass