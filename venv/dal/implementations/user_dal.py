#from ..interfaces.iuser_dal import IUserDAL
from dal.interfaces.iuser_dal import IUserDAL
from models.user import User
from models.flight import Flight
#import IUserDAL from interfaces.iuser_dal

class UserDAL(IUserDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_user_by_username(self, user_id):
        data = self.api_client.get(f"user/get{user_id}")
        return User.to_client_format(data.json())

    def create_user(self, user):
        print(f'create user: {user.to_server_format()}')
        data = self.api_client.post("user/add", user.to_server_format())   
        return User.to_client_format(data.json())

    # def update_user(self, user_id, user_data):
    #     data = self.api_client.put(f"user/{user_id}", user_data)
    #     return User(**data)

    # def delete_user(self, user_id):
    #     self.api_client.delete(f"user/{user_id}")
    #     #

    # def get_user_flights(self, user_id):
    #     data = self.api_client.get(f"user/{user_id}/flights")
    #     return [Flight(**flight_data) for flight_data in data]
