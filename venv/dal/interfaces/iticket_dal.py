from abc import ABC, abstractmethod

class ITicketDAL(ABC):
    @abstractmethod
    def get_ticket(self, ticket_id):
        pass

    @abstractmethod
    def create_ticket(self, ticket_data):
        pass

    @abstractmethod
    def update_ticket(self, ticket_id, ticket_data):
        pass

    @abstractmethod
    def delete_ticket(self, ticket_id):
        pass

    @abstractmethod
    def get_user_tickets(self, user_id):
        pass