import requests

class GeoLocation:
    def __init__(self, latitude, longitude, velocity, geo_locator_api_key):
        self.latitude = latitude
        self.longitude = longitude
        self.velocity = velocity
        self.geo_locator_api_key = geo_locator_api_key
        self.country = None
        self.city = None
        self.ocean = None

    def geo_location(self):
        api = f"https://api.opencagedata.com/geocode/v1/json?q={self.latitude}+{self.longitude}&key={self.geo_locator_api_key}"
        api_response = requests.get(api, timeout=5).json()

        components = api_response["results"][0]["components"]

        self.country = components.get("country")
        self.city = components.get("city")
        self.ocean = components.get("body_of_water")



    def print_geolocation(self):
        if self.ocean:
            return f"The ISS satellite is flying over the {self.ocean}, it's velocity is {self.velocity} km/h"
        elif self.country and self.city:
            return f"The ISS satellite is flying over the {self.city}, {self.country}, it's velocity is {self.velocity} km/h"
        else:
            return f"The ISS satellite is flying over the {self.country}, it's velocity is {self.velocity} km/h'"
