from datetime import datetime
from typing import Optional

class Ticket:
    def __init__(self, flight_id, user_id, purchase_datetime, id=None):
        self.id: Optional[int] = id
        self.flight_id = flight_id
        self.user_id = user_id
        self.purchase_datetime = purchase_datetime

    def to_server_format(self):
            
        def format_datetime(dt):
            return dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else None
        
        return {
            #"Id": str(self.id),
            "UserId": int(self.user_id),
            "FlightId": int(self.flight_id),
            "PurchaseDatetime": format_datetime(self.purchase_datetime)
        }


    @classmethod
    def to_client_format(cls, server_dict: dict) -> 'Ticket':
                
        def parse_datetime(dt_str):
            return datetime.strptime(dt_str.split('.')[0], "%Y-%m-%dT%H:%M:%S") if dt_str else None

        return cls(
            id=int(server_dict["id"]),
            flight_id=int(server_dict["flightId"]),
            user_id=int(server_dict["userId"]),
            purchase_datetime=parse_datetime(server_dict["purchaseDatetime"])
        )


    def __str__(self):
        return (f"Ticket(id={self.id}, flight_id={self.flight_id}, "
                f"user_id={self.user_id}, purchase_datetime={self.purchase_datetime.strftime('%Y-%m-%d %H:%M:%S')})")

    def __repr__(self):
        return self.__str__()  # Use the same format for both __str__ and __repr__
