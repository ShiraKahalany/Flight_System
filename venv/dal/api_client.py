import requests
from config import API_BASE_URL
from exceptions import NetworkException, UnexpectedErrorException

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL

    def _make_request(self, method, endpoint, params=None, data=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            if method == 'GET':
                response = requests.get(url, json=params)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data)
            elif method == 'DELETE':
                response = requests.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.ConnectionError):
                raise NetworkException(f"Network error: {str(e)}") from e
            elif isinstance(e, requests.exceptions.Timeout):
                raise NetworkException(f"Request timed out: {str(e)}") from e
            elif isinstance(e, requests.exceptions.HTTPError):
                # Re-raise HTTPError to be handled in DAL
                raise
            else:
                raise UnexpectedErrorException(f"Unexpected error during API request: {str(e)}") from e

    def get(self, endpoint, params=None):
        return self._make_request('GET', endpoint, params=params)

    def post(self, endpoint, data):
        headers = {'Content-Type': 'application/json'}
        return self._make_request('POST', endpoint, data=data, headers=headers)

    def put(self, endpoint, data):
        return self._make_request('PUT', endpoint, data=data)

    def delete(self, endpoint):
        return self._make_request('DELETE', endpoint)

# import requests
# from config import API_BASE_URL

# class APIClient:
#     def __init__(self):
#         self.base_url = API_BASE_URL

#     def get(self, endpoint, params=None):
#         response = requests.get(f"{self.base_url}/{endpoint}", params=params)
#         response.raise_for_status()
#         return response

#     def post(self, endpoint, data):
#         headers = {'Content-Type': 'application/json'}
#         response = requests.post(f"{self.base_url}/{endpoint}", json=data, headers=headers)
#         response.raise_for_status()
#         return response


#     def put(self, endpoint, data):
#         response = requests.put(f"{self.base_url}/{endpoint}", json=data)
#         response.raise_for_status()
#         return response

#     def delete(self, endpoint):
#         response = requests.delete(f"{self.base_url}/{endpoint}")
#         response.raise_for_status()
#         return response
