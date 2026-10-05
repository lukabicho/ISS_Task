import requests

class IssRequest:
    def __init__(self, _iss_api_endpoint):
        self.endpoint = _iss_api_endpoint
        """WITH REQUESTS.SESSION() TCP CONNECTION IS ONLY ESTABLISHED DURING THE INITIAL CALL, USING HTTP KEEP-ALIVE FOR SUBSEQUENT CALLS """
        self.session = requests.Session()

    def return_response(self):
        response = self.session.get(self.endpoint)
        response.raise_for_status()
        return response.json()