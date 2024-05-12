import logging
import psycopg2.pool
from Utils.Database.DbConfig import database_config
from Utils.Database.DatabaseStartupEvent import on_startup

# on_startup()
print('creating pool')
connection_pool = psycopg2.pool.SimpleConnectionPool(maxconn=4, minconn=1, **database_config)


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self):
        try:
            self.conn = connection_pool.getconn()
        except psycopg2.Error as err:
            logging.error(f'Error connecting to the platform (connection): {err}')
            raise

        # getting the cursor
        try:
            self.cursor = self.conn.cursor()
        except psycopg2.Error as err:
            logging.error(f'Error connecting to the platform (cursor): {err}')
        return self.conn

    def close(self):
        try:
            self.cursor.close()
            connection_pool.putconn(self.conn)
        except psycopg2.Error as err:
            print(f'Error while closing the connection: {err}')

    def commit(self):
        try:
            self.conn.commit()
        except psycopg2.Error as ce:
            print(f'Error committing changes: {ce}')

    def get_cursor(self):
        return self.cursor

    def __enter__(self) -> 'Database':
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
