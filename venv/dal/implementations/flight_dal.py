from dal.interfaces.iflight_dal import IFlightDAL
from models.flight import Flight
from models.user import User

class FlightDAL(IFlightDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_flight(self, flight):
        res = self.api_client.post("flight/add", flight)
        return Flight.to_client_format(res.json())
    
    def get_flights(self):
        res = self.api_client.get("flight/get/all")
        return [Flight.to_client_format(flight_data) for flight_data in res.json()]

    def get_flights_of_user(self, user_id):
        res = self.api_client.get(f"flight/getbyuser/{user_id}")
        return [Flight.to_client_format(flight_data) for flight_data in res.json()]
    
    def get_BGR_lands_next_5_hours(self):
        res = self.api_client.get("flight/next5hours")
        return [Flight.to_client_format(flight_data) for flight_data in res.json()]
    
    def get_flight_by_id(self, flight_id):
        res = self.api_client.get(f"flight/get/{flight_id}")
        return Flight.to_client_format(res.json())

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