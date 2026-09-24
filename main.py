import os
from dotenv import load_dotenv
import logging
from time import perf_counter, sleep
from IssRequest import IssRequest
from GeoLocation import GeoLocation
from JsonReader import JsonReader
from JsonWriter import JsonWriter
from DatabaseConnector import DatabaseConnector

def main():
    load_dotenv()

    iss_api_key=os.getenv("ISS_API_KEY")
    geo_locator_api_key = os.getenv("GEO_LOCATOR_API_KEY")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("iss_tracker.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    db_config = {
        "dbname": os.getenv("DBNAME"),
        "user": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT", 5432)
    }

    db_conn = DatabaseConnector(db_config)
    iss_api_call = IssRequest(iss_api_key)
    json_reader = JsonReader("satellite_data.jsonl")
    json_writer = JsonWriter("satellite_data.jsonl")
    time_interval = 15

    while True:
        start = perf_counter()

        iss_api_fetch = iss_api_call.return_response()


        json_writer.json_write(iss_api_fetch)


        for unread_record in json_reader.json_read(db_conn.get_latest_timestamp()):
            locator = GeoLocation(unread_record["latitude"], unread_record["longitude"],
                                       unread_record["velocity"], geo_locator_api_key=geo_locator_api_key)
            locator.geo_location()
            location_text = locator.print_geolocation()
            db_conn.insert_in_raw_table(unread_record)
            logging.info(location_text)

            traveled_distance = db_conn.last_velocity() * (db_conn.get_last_elapsed_seconds() / 3600)
            if traveled_distance > 0:
                traveled_distance_text = f"The satellite has traveled {traveled_distance} kilometers in the last {db_conn.get_last_elapsed_seconds()} seconds"
                db_conn.insert_in_human_table(location_text, traveled_distance_text)
                logging.info(traveled_distance_text)
            else:
                logging.info("This is the first record, wait to see traveled distance")

        logging.info(f"The satellite is more often in the {db_conn.often_visibility()} state ")

        end = perf_counter()
        print(end - start)
        sleep(time_interval)

if __name__ == '__main__':
    main()