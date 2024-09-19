from abc import ABC, abstractmethod

class IFlightDAL(ABC):

    @abstractmethod
    def create_flight(self, flight_data):
        pass

    @abstractmethod
    def get_flights(self):
        pass

    @abstractmethod
    def get_flights_of_user(self, user_id):
        pass

    # @abstractmethod
    # def get_flight(self, flight_id):
    #     pass

    # @abstractmethod
    # def update_flight(self, flight_id, flight_data):
    #     pass

    # @abstractmethod
    # def delete_flight(self, flight_id):
    #     pass

    # @abstractmethod
    # def get_upcoming_landings(self, hours_ahead):
    #     pass

    # @abstractmethod
    # def get_flight_passengers(self, flight_id):
    #     pass


