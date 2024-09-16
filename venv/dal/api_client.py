import requests
from config import API_BASE_URL

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL

    def get(self, endpoint, params=None):
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    #def post(self, endpoint, data):
        # headers = {'Content-Type': 'application/json'}
        # response = requests.post(f"{self.base_url}/{endpoint}", json=data, headers=headers)
        # response.raise_for_status()
        # return response.json()
    def post(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        print(f"Sending POST request to {url}")
        print(f"Headers: {headers}")
        print(f"Data: {data}")
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()


    def put(self, endpoint, data):
        response = requests.put(f"{self.base_url}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        response = requests.delete(f"{self.base_url}/{endpoint}")
        response.raise_for_status()
        return response.json()




#class APIClient(IDAL):
    # @staticmethod
    # def get_flights():
    #     response = requests.get(f"{API_BASE_URL}/flights")
    #     response.raise_for_status()
    #     return response.json()

    # @staticmethod
    # def book_flight(flight_id, user_id):
    #     response = requests.post(f"{API_BASE_URL}/flights/book", json={
    #         "flightId": flight_id,
    #         "userId": user_id
    #     })
    #     response.raise_for_status()
    #     return response.json()

    # @staticmethod
    # def add_aircraft(manufacturer, nickname, year_of_manufacture, image_url):
    #     response = requests.post(f"{API_BASE_URL}/aircraft", json={
    #         "manufacturer": manufacturer,
    #         "nickname": nickname,
    #         "year_of_manufacture": year_of_manufacture,
    #         "image_url": image_url
    #     })
    #     response.raise_for_status()
    #     return response.json()

    # @staticmethod
    # def get_user_flights(user_id):
    #     response = requests.get(f"{API_BASE_URL}/users/{user_id}/flights")
    #     response.raise_for_status()
    #     return response.json()
