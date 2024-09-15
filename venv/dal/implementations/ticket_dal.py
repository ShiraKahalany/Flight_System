from dal.interfaces.iticket_dal import ITicketDAL
from models.ticket import Ticket

class TicketDAL(ITicketDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_ticket(self, ticket_id):
        data = self.api_client.get(f"tickets/{ticket_id}")
        return Ticket(**data)

    def create_ticket(self, ticket_data):
        data = self.api_client.post("tickets", ticket_data)
        return Ticket(**data)

    def update_ticket(self, ticket_id, ticket_data):
        data = self.api_client.put(f"tickets/{ticket_id}", ticket_data)
        return Ticket(**data)

    def delete_ticket(self, ticket_id):
        self.api_client.delete(f"tickets/{ticket_id}")

    def get_user_tickets(self, user_id):
        data = self.api_client.get(f"users/{user_id}/tickets")
        return [Ticket(**ticket_data) for ticket_data in data]