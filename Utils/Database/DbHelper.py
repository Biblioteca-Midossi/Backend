import logging
import mysql.connector as mysql
from Utils.Database.DbConfig import database_config
from Utils.Database.DatabaseStartupEvent import on_startup

on_startup()
print('creating pool')
connection_pool = mysql.pooling.MySQLConnectionPool(pool_name = "pool", **database_config)


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self):
        try:
            self.conn = connection_pool.get_connection()
        except mysql.Error as err:
            logging.error(f'Error connecting to the platform (connection): {err}')
            raise

        # getting the cursor
        try:
            self.cursor = self.conn.cursor(buffered = True)
        except mysql.Error as err:
            logging.error(f'Error connecting to the platform (cursor): {err}')
        return self.conn

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except mysql.Error as err:
            print(f'Error while closing the connection: {err}')

    def commit(self):
        try:
            self.conn.commit()
        except mysql.Error as ce:
            print(f'Error committing changes: {ce}')

    def get_cursor(self):
        return self.cursor

    def __enter__(self) -> 'Database':
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
