# db/connection.py

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class DBConnection:
    _instance = None

    def __init__(self):
        if DBConnection._instance is not None:
            raise Exception("Usa DBConnection.get_instance() para obtener la conexión")
        self._connection = psycopg2.connect(DATABASE_URL)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_connection(self):
        return self._connection