from abc import ABC, abstractmethod

class IUserDAL(ABC):

    @abstractmethod
    def login_user(self, user_id):
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


