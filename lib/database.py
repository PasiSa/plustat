import sqlite3
from sqlite3 import Error
from lib.settings import settings

class Database():
    def __init__(self):
        #from main import settings
        self.connection = sqlite3.connect(settings.DB_FILE)

    def write_query(self, query: str) -> None:
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        #print("Query executed successfully")

    def read_query(self, query: str) -> list:
        cursor = self.connection.cursor()
        result = None
        cursor.execute(query)
        result = cursor.fetchall()
        return result
