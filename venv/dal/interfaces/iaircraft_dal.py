from abc import ABC, abstractmethod

class IAircraftDAL(ABC):

    @abstractmethod
    def create_aircraft(self, aircraft_data):
        pass

    # @abstractmethod
    # def get_aircraft(self, aircraft_id):
    #     pass

    # @abstractmethod
    # def update_aircraft(self, aircraft_id, aircraft_data):
    #     pass

    # @abstractmethod
    # def delete_aircraft(self, aircraft_id):
    #     pass

    # @abstractmethod
    # def get_aircraft_flights(self, aircraft_id):
    #     pass

    # @abstractmethod
    # def get_image_tags(self, image_url):
    #     pass


