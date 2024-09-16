from abc import ABC, abstractmethod
from datetime import datetime

class IDateDetailsDAL(ABC):
    @abstractmethod
    def get_date_details(self, date: datetime, location: str):
        pass