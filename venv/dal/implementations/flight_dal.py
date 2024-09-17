from dal.interfaces.iflight_dal import IFlightDAL
from models.flight import Flight
from models.user import User

class FlightDAL(IFlightDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_flight(self, flight_id):
        data = self.api_client.get(f"flight/get{flight_id}")
        return Flight(**data)

    def create_flight(self, flight_data):
        data = self.api_client.post("flight/add", flight_data)
        return Flight(**data)

    # def update_flight(self, flight_id, flight_data):
    #     data = self.api_client.put(f"flight/{flight_id}", flight_data)
    #     return Flight(**data)

    def delete_flight(self, flight_id):
        self.api_client.delete(f"flight/delete{flight_id}")

    # def get_upcoming_landings(self, hours_ahead):
    #     data = self.api_client.get("flight/upcoming_landings", {"hours_ahead": hours_ahead})
    #     return [Flight(**flight_data) for flight_data in data]

    # def get_flight_passengers(self, flight_id):
    #     data = self.api_client.get(f"flight/{flight_id}/passengers")
    #     return [User(**user_data) for user_data in data]