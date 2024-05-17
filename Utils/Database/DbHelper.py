import logging
import psycopg2.pool
from Utils.Database.DbConfig import database_config
from Utils.Database.DatabaseStartupEvent import on_startup

log = logging.getLogger('FileLogger')

# on_startup()
log.info('Createing connection pool..')
connection_pool = psycopg2.pool.SimpleConnectionPool(maxconn=4, minconn=1, **database_config)
log.info('Pool successfully created!')


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self):
        # getting a connection from the pool
        try:
            self.conn = connection_pool.getconn()
        except psycopg2.Error as pool_error:
            log.error(f'Error while getting a connection from the pool: {pool_error}')
            raise

        # getting the cursor
        try:
            self.cursor = self.conn.cursor()
        except psycopg2.Error as cursor_error:
            log.error(f'Error while getting the cursor from the connection: {cursor_error}')
        return self.conn

    def close(self):
        try:
            self.cursor.close()
            connection_pool.putconn(self.conn)
        except psycopg2.Error as close_error:
            print(f'Error while closing the cursor or the connection: {close_error}')

    def commit(self):
        try:
            self.conn.commit()
        except psycopg2.Error as commit_error:
            print(f'Error while committing changes to the database: {commit_error}')

    def get_cursor(self):
        return self.cursor

    def __enter__(self) -> 'Database':
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
