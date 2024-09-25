from dal.interfaces.iflight_dal import IFlightDAL
from models.flight import Flight
from models.user import User
from exceptions import FlightCreationException, FlightNotFoundException, FlightRetrievalException, NetworkException, UnexpectedErrorException
import requests
import json

class FlightDAL(IFlightDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_flight(self, flight: Flight):
        try:
            res = self.api_client.post("flight/add", flight.to_server_format())
            return Flight.to_client_format(res.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise FlightCreationException(f"Invalid flight data: {e.response.text}") from e
            else:
                raise FlightCreationException(f"Flight creation failed: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during flight creation: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during flight creation: {e}") from e
    
    def get_flights(self):
        try:
            res = self.api_client.get("flight/get/all")
            return [Flight.to_client_format(flight_data) for flight_data in res.json()]
        except requests.exceptions.HTTPError as e:
            raise FlightRetrievalException(f"Failed to retrieve flights: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during flight retrieval: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during flight retrieval: {e}") from e

    def get_flights_of_user(self, user_id):
        try:
            res = self.api_client.get(f"flight/getbyuser/{user_id}")
            return [Flight.to_client_format(flight_data) for flight_data in res.json()]
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise FlightNotFoundException(f"No flights found for user {user_id}") from e
            else:
                raise FlightRetrievalException(f"Failed to retrieve user flights: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during user flight retrieval: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during user flight retrieval: {e}") from e
    
    def get_BGR_lands_next_5_hours(self):
        try:
            res = self.api_client.get("flight/next5hours")
            return [Flight.to_client_format(flight_data) for flight_data in res.json()]
        except requests.exceptions.HTTPError as e:
            raise FlightRetrievalException(f"Failed to retrieve BGR flights for next 5 hours: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during BGR flight retrieval: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during BGR flight retrieval: {e}") from e
    
    def get_flight_by_id(self, flight_id):
        try:
            res = self.api_client.get(f"flight/get/{flight_id}")
            return Flight.to_client_format(res.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise FlightNotFoundException(f"Flight with id {flight_id} not found") from e
            else:
                raise FlightRetrievalException(f"Failed to retrieve flight: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during flight retrieval: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during flight retrieval: {e}") from e

    
    def is_landing_delayed(self, flight_details): 
        try:
            #flight_details = json.dumps(flight_details)
            #headers = {'Content-Type': 'application/json'}
            res = self.api_client.post(f"prediction/", data=flight_details)
            return res.json()
        except requests.exceptions.HTTPError as e:
            raise FlightRetrievalException(f"Failed to retrieve flight delay status: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during flight delay status retrieval: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during flight delay status retrieval: {e}") from e

    # def update_flight(self, flight_id, flight_data):
    #     data = self.api_client.put(f"flight/{flight_id}", flight_data)
    #     return Flight(**data)

    # def get_flight(self, flight_id):
    #     data = self.api_client.get(f"flight/get{flight_id}")
    #     return Flight(**data)

    # def delete_flight(self, flight_id):
    #     self.api_client.delete(f"flight/delete{flight_id}")

    # def get_upcoming_landings(self, hours_ahead):
    #     data = self.api_client.get("flight/upcoming_landings", {"hours_ahead": hours_ahead})
    #     return [Flight(**flight_data) for flight_data in data]

    # def get_flight_passengers(self, flight_id):
    #     data = self.api_client.get(f"flight/{flight_id}/passengers")
    #     return [User(**user_data) for user_data in data]