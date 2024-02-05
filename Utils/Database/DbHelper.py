import logging
from typing import Optional, Dict

import mysql.connector as mysql

from dotenv import get_key

database_config: Dict[str, Optional[str]] = {
    "database": get_key('.env', 'DBNAME'),
    "user": get_key('.env', 'USER'),
    "password": get_key('.env', 'PASSWORD'),
    "host": get_key('.env', 'HOST'),
    "port": get_key('.env', 'PORT'),
}


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self):
        try:
            self.conn = mysql.connect(**database_config)
        except mysql.Error as err:
            logging.error(f'Error connecting to the platform (connection): {err}')
            raise

        # getting the cursor
        try:
            self.cursor = self.conn.cursor()
        except mysql.Error as err:
            logging.error(f'Error connecting to the platform (cursor): {err}')
        return self.conn

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except mysql.Error as err:
            print(f'Error while closing the connection: {err}')

    def get_cursor(self):
        return self.cursor

    def __enter__(self) -> 'Database':
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
