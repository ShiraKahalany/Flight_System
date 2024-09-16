#from ..interfaces.iuser_dal import IUserDAL
from dal.interfaces.iuser_dal import IUserDAL
from models.user import User
from models.flight import Flight
#import IUserDAL from interfaces.iuser_dal

class UserDAL(IUserDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_user(self, user_id):
        data = self.api_client.get(f"users/{user_id}")
        return User(**data)

    def create_user(self, user_data):
        data = self.api_client.post("users", user_data)
        return User(**data)

    def update_user(self, user_id, user_data):
        data = self.api_client.put(f"users/{user_id}", user_data)
        return User(**data)

    def delete_user(self, user_id):
        self.api_client.delete(f"users/{user_id}")
        #

    def get_user_flights(self, user_id):
        data = self.api_client.get(f"users/{user_id}/flights")
        return [Flight(**flight_data) for flight_data in data]
