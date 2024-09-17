class Ticket:
    def __init__(self, id, flight_id, user_id, purchase_datetime):
        self.id = id
        self.flight_id = flight_id
        self.user_id = user_id
        self.purchase_datetime = purchase_datetime

    def __str__(self):
        return (f"Ticket(id={self.id}, flight_id={self.flight_id}, "
                f"user_id={self.user_id}, purchase_datetime={self.purchase_datetime.strftime('%Y-%m-%d %H:%M:%S')})")

    def __repr__(self):
        return self.__str__()  # Use the same format for both __str__ and __repr__
