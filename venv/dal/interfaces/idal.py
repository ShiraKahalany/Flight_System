from abc import ABC, abstractmethod
from .iuser_dal import IUserDAL
from .iflight_dal import IFlightDAL
from .iaircraft_dal import IAircraftDAL
from .iticket_dal import ITicketDAL
from .idate_details_dal import IDateDetailsDAL
from .iimage_recognition_dal import IImageRecognitionDAL

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

    @property
    @abstractmethod
    def DateDetails(self) -> IDateDetailsDAL:
        pass

    @property
    @abstractmethod
    def ImageRecognition(self) -> IImageRecognitionDAL:
        pass
