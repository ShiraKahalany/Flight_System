from dal.interfaces.iuser_dal import IUserDAL
from models.user import User
from exceptions import UserCreationException, UserAlreadyExistsException, NetworkException, UnexpectedErrorException,UserNotFoundException, InvalidCredentialsException
import requests

class UserDAL(IUserDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_user(self, user):
        try:
            print(f'create user: {user.to_server_format()}')
            data = self.api_client.post("user/add", user.to_server_format())   
            return User.to_client_format(data.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:  # Assuming 409 is used for "Conflict" (user already exists)
                raise UserAlreadyExistsException(f"User with username '{user.username}' already exists")
            elif e.response.status_code == 400:
                raise UserCreationException(f"Invalid user data: {e.response.text}")
            else:
                raise UserCreationException(f"User creation failed: {e}")
        except NetworkException as e:
            raise NetworkException(f"Network error during user creation: {e}")
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during user creation: {e}")

    def login_user(self, username, password):
        try:
            data = self.api_client.get(f"user/login?username={username}&password={password}")
            return User.to_client_format(data.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise UserNotFoundException("User not found") from e
            elif e.response.status_code == 401:
                raise InvalidCredentialsException("Invalid username or password") from e
            else:
                raise UnexpectedErrorException(f"Unexpected error during login: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during login: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during login: {e}") from e

    # def update_user(self, user_id, user_data):
    #     data = self.api_client.put(f"user/{user_id}", user_data)
    #     return User(**data)

    # def delete_user(self, user_id):
    #     self.api_client.delete(f"user/{user_id}")
    #     #

    # def get_user_flights(self, user_id):
    #     data = self.api_client.get(f"user/{user_id}/flights")
    #     return [Flight(**flight_data) for flight_data in data]
