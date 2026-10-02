import json

class JsonWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def json_write(self, data):
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(json.dumps(data, ensure_ascii=False) + "\n")