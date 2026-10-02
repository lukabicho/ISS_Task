import os
from dotenv import load_dotenv

load_dotenv()

class DbConfig:
        db_config = {
                "dbname": os.getenv("DBNAME"),
                "user": os.getenv("USERNAME"),
                "password": os.getenv("PASSWORD"),
                "host": os.getenv("HOST"),
                "port": os.getenv("PORT", 5432)
            }