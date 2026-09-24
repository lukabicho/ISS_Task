import json

class JsonWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def json_write(self, data):
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(json.dumps(data, ensure_ascii=False) + "\n")


# def json_write(self, file_name):
#     with open(file_name, "r+", encoding="utf-8") as file:
#         file.seek(0)
#         first_char = file.read(1)
#
#         while first_char and first_char.isspace():
#             first_char = file.read(1)
#
#         if first_char != "[":
#             file.seek(0)
#             file.truncate()
#             file.write("[\n")
#             json.dump(self.iss_api_endpoint.json(), file, indent=4)
#             file.write("\n]")
#         else:
#
#             file.seek(0, os.SEEK_END)
#             pos = file.tell()
#
#             while pos > 0:
#                 pos -= 1
#                 file.seek(pos)
#                 char = file.read(1)
#                 if char == "]":
#                     file.seek(pos)
#                     file.truncate()
#                     break
#
#             if first_char == "[":
#                 file.write(",\n")
#                 json.dump(self.iss_api_endpoint.json(), file, indent=4)
#                 file.write("\n]")
#             else:
#                 file.write("\n")
#                 json.dump(self.iss_api_endpoint.json(), file, indent=4)