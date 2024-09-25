from dal.interfaces.iticket_dal import ITicketDAL
from models.ticket import Ticket
from exceptions import TicketCreationException,TicketRetrievalException, NetworkException, UnexpectedErrorException, TicketNotFoundException
import requests

class TicketDAL(ITicketDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_ticket(self, ticket: Ticket):
        try:
            data = self.api_client.post("ticket/add", ticket.to_server_format())    
            return Ticket.to_client_format(data.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise TicketCreationException(f"Invalid ticket data: {e.response.text}") from e
            else:
                raise TicketCreationException(f"Ticket creation failed: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during ticket creation: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during ticket creation: {e}") from e

    def get_tickets(self):
        try:
            res = self.api_client.get("ticket/get/all")
            return [Ticket.to_client_format(ticket_data) for ticket_data in res.json()]
        except requests.exceptions.HTTPError as e:
            raise TicketRetrievalException(f"Failed to retrieve tickets: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during ticket retrieval: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during ticket retrieval: {e}") from e
    
    def get_ticket(self, ticket_id):
        data = self.api_client.get(f"ticket/{ticket_id}")
        return Ticket(**(data.json()))

    def get_user_tickets(self, user_id):
        try:
            res = self.api_client.get(f"ticket/getbyuser/{user_id}")
            return [Ticket.to_client_format(ticket_data) for ticket_data in res.json()]
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise TicketNotFoundException(f"No flights found for user {user_id}") from e
            else:
                raise TicketRetrievalException(f"Failed to retrieve user flights: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during user flight retrieval: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during user flight retrieval: {e}") from e

            
    def delete_ticket(self, ticket_id):
        try:
            self.api_client.delete(f"ticket/delete/{ticket_id}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise TicketNotFoundException(f"Ticket with id {ticket_id} not found") from e
            else:
                raise TicketRetrievalException(f"Failed to delete ticket") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during ticket deletion: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during ticket deletion: {e}") from e
        
   
   
   
   
    # def update_ticket(self, ticket_id, ticket_data):
    #     data = self.api_client.put(f"ticket/{ticket_id}", ticket_data)
    #     return Ticket(**data)

    # def delete_ticket(self, ticket_id):
    #     self.api_client.delete(f"ticket/{ticket_id}")