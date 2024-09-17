from abc import ABC, abstractmethod
from datetime import datetime
from models.hebrew_times import DateDetails

class IDateDetailsDAL(ABC):
    @abstractmethod
    def get_date_details(self, date: datetime, location: str) -> DateDetails:
        pass