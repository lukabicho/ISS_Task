import requests
import os
from dotenv import load_dotenv
import logging
import json
from time import perf_counter, sleep
import psycopg
from psycopg.rows import dict_row

load_dotenv()

GEO_LOCATOR_API_KEY = os.getenv("GEO_LOCATOR_API_KEY")

# logging.basicConfig(level=logging.DEBUG)

db_config = {
    "dbname": os.getenv("DBNAME"),
    "user": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT", 5432)
}

class IssRequest:
    def __init__(self):
        self.response = requests.get("https://api.wheretheiss.at/v1/satellites/25544?")

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
    def __init__(self, latitude, longitude, velocity, _GEO_LOCATOR_API_KEY, id):
        self.latitude = latitude
        self.longitude = longitude
        self.velocity = velocity
        self.GEO_LOCATOR_API_KEY = _GEO_LOCATOR_API_KEY
        self.country = None
        self.city = None
        self.ocean = None

    def geo_location(self):
        location = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={self.latitude}+{self.longitude}&key="
                                f"{self.GEO_LOCATOR_API_KEY}")

        location_json = location.text
        locator_data = json.loads(location_json)

        first_parse = locator_data["results"][0]
        components = first_parse["components"]

        self.country = components.get("country")
        self.city = components.get("city")
        self.ocean = components.get("body_of_water")

    def print_geolocation(self):
        if self.ocean:
            print(f"The ISS is above {self.ocean}, it's current speed is {self.velocity} kmh")
        elif self.country and self.city:
            print(
                f"The ISS is above {self.country}, {self.city}, it's current speed is {self.velocity} kmh")
        else:
            print(f"The ISS is above{self.country}, it's current speed is {self.velocity} kmh")


class DatabaseConnection:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def insert_in_db(self, latitude, longitude, velocity):

        self.latitude = latitude
        self.longitude = longitude
        self.velocity = velocity



        with (psycopg.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password)
        as conn):
            with conn.cursor() as cursor:

                cursor.execute("""CREATE TABLE IF NOT EXISTS iss_loccall
                        (lat FLOAT, 
                        lng FLOAT,
                        vel FLOAT
                        )""")

                cursor.execute("""INSERT INTO iss_loccall VALUES (%s,%s,%s)""", (self.latitude, self.longitude, self.velocity) )
            conn.commit()

    def return_table(self):
        with (psycopg.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            )
        as conn):
            with conn.cursor(row_factory=dict_row) as cursor:

                cursor.execute("""SELECT * FROM iss_loccall ORDER BY id DESC""")
                self.a = cursor.fetchone()

while True:
    # response = IssRequest().response
    start = perf_counter()

    iss_api_fetch = IssResponse(requests.get("https://api.wheretheiss.at/v1/satellites/25544?"))
    iss_api_fetch.json_write("satelite_data.json")
    json_fetch = JsonFetcher("satelite_data.json")
    json_fetch.extract_location()

    db_conn = DatabaseConnection(**db_config)
    db_conn.insert_in_db(json_fetch.latitude, json_fetch.longitude, json_fetch.velocity)
    db_conn.return_table()


    geo_location = GeoLocation(_GEO_LOCATOR_API_KEY = GEO_LOCATOR_API_KEY, **db_conn.a)
    geo_location.geo_location()
    print(geo_location.ocean, geo_location.country, geo_location.city)
    geo_location.print_geolocation()

    end = perf_counter()
    print(end - start)
    sleep(5)