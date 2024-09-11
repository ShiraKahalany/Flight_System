from datetime import datetime

class Ticket:
    def __init__(self, id, flight_id, user_id, purchase_datetime):
        self.id = id
        self.flight_id = flight_id
        self.user_id = user_id
        self.purchase_datetime = purchase_datetime