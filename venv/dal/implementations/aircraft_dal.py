from dal.interfaces.iaircraft_dal import IAircraftDAL
from models.aircraft import Aircraft
from models.flight import Flight
from exceptions import AircraftCreationException, AircraftRetrievalException, AircraftNotFoundException, NetworkException, UnexpectedErrorException
import requests

class AircraftDAL(IAircraftDAL):
    def __init__(self, api_client):
        self.api_client = api_client
    
    def create_aircraft(self, aircraft):
        try:
            res = self.api_client.post("aircraft/add", aircraft.to_server_format())
            return Aircraft.to_client_format(res.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise AircraftCreationException(f"Invalid aircraft data: {e.response.text}") from e
            else:
                raise AircraftCreationException(f"Aircraft creation failed: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during aircraft creation: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during aircraft creation: {e}") from e
    
    def get_aircrafts(self):
        try:
            res = self.api_client.get("aircraft/get/all")
            return [Aircraft.to_client_format(aircraft_data) for aircraft_data in res.json()]
        except requests.exceptions.HTTPError as e:
            raise AircraftRetrievalException(f"Failed to retrieve aircrafts: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during aircraft retrieval: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during aircraft retrieval: {e}") from e

    def get_aircraft_by_id(self, aircraft_id):
        try:
            res = self.api_client.get(f"aircraft/get/{aircraft_id}")
            return Aircraft.to_client_format(res.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise AircraftNotFoundException(f"Aircraft with id {aircraft_id} not found") from e
            else:
                raise AircraftRetrievalException(f"Failed to retrieve aircraft: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during aircraft retrieval: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during aircraft retrieval: {e}") from e
    
    # def get_aircraft(self, aircraft_id):
    #     data = self.api_client.get(f"aircraft/get/{aircraft_id}")
    #     print(f'the dataaaa:  {data.json()}')
    #     return Aircraft(**(data.json()))

    # def update_aircraft(self, aircraft_id, aircraft_data):
    #     data = self.api_client.put(f"aircraft/{aircraft_id}", aircraft_data)
    #     return Aircraft(**data)

    # def delete_aircraft(self, aircraft_id):
    #     self.api_client.delete(f"aircraft/delete/{aircraft_id}")

    # def get_aircraft_flights(self, aircraft_id):
    #     data = self.api_client.get(f"aircraft/{aircraft_id}/flights")
    #     return [Flight(**flight_data) for flight_data in data]

    # def get_image_tags(self, image_url):
    #     data = self.api_client.get(f"image-tags", params={"url": image_url})
    #     return data['tags']