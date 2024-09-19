from datetime import datetime
from typing import Optional

class Ticket:
    def __init__(self, flight_id, user_id, purchase_datetime, id=None):
        self.id: Optional[int] = id
        self.flight_id = flight_id
        self.user_id = user_id
        self.purchase_datetime = purchase_datetime

    def to_server_format(self):
        return {
            #"Id": str(self.id),
            "UserId": str(self.user_id),
            "FlightId": str(self.flight_id),
            "PurchaseDatetime": self.purchase_datetime.isoformat()
        }

    @classmethod
    def to_client_format(cls, server_dict):
        return cls(
            id=int(server_dict["id"]),
            flight_id=int(server_dict["flightId"]),
            user_id=int(server_dict["userId"]),
            purchase_datetime=datetime.fromisoformat(server_dict["PurchaseDateTime"])
        )


    def __str__(self):
        return (f"Ticket(id={self.id}, flight_id={self.flight_id}, "
                f"user_id={self.user_id}, purchase_datetime={self.purchase_datetime.strftime('%Y-%m-%d %H:%M:%S')})")

    def __repr__(self):
        return self.__str__()  # Use the same format for both __str__ and __repr__
