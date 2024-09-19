from dal.interfaces.iticket_dal import ITicketDAL
from models.ticket import Ticket

class TicketDAL(ITicketDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    # def get_ticket(self, ticket_id):
    #     data = self.api_client.get(f"ticket/{ticket_id}")
    #     return Ticket(**(data.json()))

    def create_ticket(self, ticket):
        data = self.api_client.post("ticket/add", ticket.to_server_format())    
        return Ticket.to_client_format(data.json())

    # def update_ticket(self, ticket_id, ticket_data):
    #     data = self.api_client.put(f"ticket/{ticket_id}", ticket_data)
    #     return Ticket(**data)

    # def delete_ticket(self, ticket_id):
    #     self.api_client.delete(f"ticket/{ticket_id}")

    # def get_user_tickets(self, user_id):
    #     data = self.api_client.get(f"user/{user_id}/tickets")
    #     return [Ticket(**ticket_data) for ticket_data in data]