from abc import ABC, abstractmethod

class IUserDAL(ABC):
    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def create_user(self, user_data):
        pass

    @abstractmethod
    def update_user(self, user_id, user_data):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def get_user_flights(self, user_id):
        pass


class IFlightDAL(ABC):
    @abstractmethod
    def get_flight(self, flight_id):
        pass

    @abstractmethod
    def create_flight(self, flight_data):
        pass

    @abstractmethod
    def update_flight(self, flight_id, flight_data):
        pass

    @abstractmethod
    def delete_flight(self, flight_id):
        pass

    @abstractmethod
    def get_upcoming_landings(self, hours_ahead):
        pass

    @abstractmethod
    def get_flight_passengers(self, flight_id):
        pass


class IAircraftDAL(ABC):
    @abstractmethod
    def get_aircraft(self, aircraft_id):
        pass

    @abstractmethod
    def create_aircraft(self, aircraft_data):
        pass

    @abstractmethod
    def update_aircraft(self, aircraft_id, aircraft_data):
        pass

    @abstractmethod
    def delete_aircraft(self, aircraft_id):
        pass

    @abstractmethod
    def get_aircraft_flights(self, aircraft_id):
        pass

    @abstractmethod
    def get_image_tags(self, image_url):
        pass



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

class IDAL(IUserDAL, IFlightDAL, IAircraftDAL, ITicketDAL):
    pass