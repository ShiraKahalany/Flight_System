from dal.idal import IAircraftDAL
from models.aircraft import Aircraft
from models.flight import Flight

class AircraftDAL(IAircraftDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_aircraft(self, aircraft_id):
        data = self.api_client.get(f"aircraft/{aircraft_id}")
        return Aircraft(**data)

    def create_aircraft(self, aircraft_data):
        data = self.api_client.post("aircraft", aircraft_data)
        return Aircraft(**data)

    def update_aircraft(self, aircraft_id, aircraft_data):
        data = self.api_client.put(f"aircraft/{aircraft_id}", aircraft_data)
        return Aircraft(**data)

    def delete_aircraft(self, aircraft_id):
        self.api_client.delete(f"aircraft/{aircraft_id}")

    def get_aircraft_flights(self, aircraft_id):
        data = self.api_client.get(f"aircraft/{aircraft_id}/flights")
        return [Flight(**flight_data) for flight_data in data]

    def get_image_tags(self, image_url):
        data = self.api_client.get(f"image-tags", params={"url": image_url})
        return data['tags']