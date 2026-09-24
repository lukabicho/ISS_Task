import requests

class IssRequest:
    def __init__(self, _iss_api_endpoint):
        self.endpoint = _iss_api_endpoint
        self.session = requests.Session()

    def return_response(self):
        response = self.session.get(self.endpoint)
        response.raise_for_status()
        return response.json()