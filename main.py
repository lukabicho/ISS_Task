import requests
import os
from dotenv import load_dotenv
import logging
import json

load_dotenv()

GEO_LOCATOR_API_KEY = os.getenv("GEO_LOCATOR_API_KEY")
response = requests.get("https://api.wheretheiss.at/v1/satellites/25544?")

class IssResponse:
    def __init__(self, _iss_api_endpoint):
        self.iss_api_endpoint = _iss_api_endpoint

    def json_write(self, file_name):
        with open(file_name, "r+", encoding="utf-8") as file:
            file.seek(0)
            first_char = file.read(1)

            while first_char and first_char.isspace():
                first_char = file.read(1)

            if first_char != "[":
                file.seek(0)
                file.truncate()
                file.write("[\n")
                json.dump(self.iss_api_endpoint.json(), file, indent=4)
                file.write("\n]")
            else:

                file.seek(0, os.SEEK_END)
                pos = file.tell()

                while pos > 0:
                    pos -= 1
                    file.seek(pos)
                    char = file.read(1)
                    if char == "]":
                        file.seek(pos)
                        file.truncate()
                        break

                if first_char == "[":
                    file.write(",\n")
                    json.dump(self.iss_api_endpoint.json(), file, indent=4)
                    file.write("\n]")
                else:
                    file.write("\n")
                    json.dump(self.iss_api_endpoint.json(), file, indent=4)

class JsonFetcher:
    def __init__(self, file_name):
        self.file_name = file_name
        self.latitude = None
        self.longitude = None
        self.velocity = None

    def extract_location(self):
        with open(self.file_name, "r+", encoding="utf-8") as file:
            json_rows = json.load(file)
            json_rows_length = len(json_rows)

            if json_rows_length > 0:
                self.latitude = json_rows[json_rows_length-1]["latitude"]
                self.longitude = json_rows[json_rows_length-1]["longitude"]
                self.velocity = json_rows[json_rows_length-1]["velocity"]
            else:
                self.latitude = json_rows[0]["latitude"]
                self.longitude = json_rows[0]["longitude"]
                self.velocity = json_rows[0]["velocity"]




class GeoLocation:
    def __init__(self, latitude, longitude, velocity, _GEO_LOCATOR_API_KEY):
        self.latitude = latitude
        self.longitude = longitude
        self.velocity = velocity
        self.GEO_LOCATOR_API_KEY = _GEO_LOCATOR_API_KEY
        self.country = None
        self.city = None
        self.ocean = None

    def geo_location(self):
        location = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={self.latitude}+{self.longitude}&key={self.GEO_LOCATOR_API_KEY}")

        location_json = location.text
        locator_data = json.loads(location_json)

        first_parse = locator_data["results"][0]
        components = first_parse["components"]

        self.country = components.get("country")
        self.city = components.get("city")
        self.ocean = components.get("body_of_water")




iss_api_fetch = IssResponse(response)
iss_api_fetch.json_write("satelite_data.json")
json_fetch = JsonFetcher("satelite_data.json")
json_fetch.extract_location()
print(json_fetch.latitude)

geo_location = GeoLocation(json_fetch.latitude, json_fetch.longitude, json_fetch.velocity, GEO_LOCATOR_API_KEY)
geo_location.geo_location()
print(geo_location.ocean, geo_location.country, geo_location.city)

if geo_location.ocean:
    print(f"The ISS is above {geo_location.ocean}, it's current speed is {geo_location.velocity}")
elif geo_location.country and geo_location.city:
    print(f"The ISS is above {geo_location.country}, {geo_location.city}, it's current speed is {geo_location.velocity}")
else:
    print(f"The ISS is above{ geo_location.country}, it's current speed is {geo_location.velocity}")

