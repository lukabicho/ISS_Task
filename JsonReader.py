import json

class JsonReader:
    def __init__(self, file_name):
        self.file_name = file_name

    def json_read(self, latest_timestamp):
        with open(self.file_name, "r", encoding="utf-8") as file:
            for line in file:
                record = json.loads(line)
                if record["timestamp"] > latest_timestamp:
                    yield record