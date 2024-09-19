from abc import ABC, abstractmethod

class IUserDAL(ABC):

    @abstractmethod
    def get_user_by_username(self, user_id):
        pass

    @abstractmethod
    def create_user(self, user_data):
        pass

    

    # @abstractmethod
    # def update_user(self, user_id, user_data):
    #     pass

    # @abstractmethod
    # def delete_user(self, user_id):
    #     pass

    # @abstractmethod
    # def get_user_flights(self, user_id):
    #     pass


