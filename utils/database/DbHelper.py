import logging
import psycopg2.pool
import redis.exceptions
from redis import Redis

from utils.database.DbConfig import psql_config, redis_config

# from Utils.Database.DatabaseStartupEvent import on_startup

log = logging.getLogger('FileLogger')

# on_startup()
log.info('Creating connection pool for postgres..')
psql_pool = psycopg2.pool.SimpleConnectionPool(maxconn = 4, minconn = 1, **psql_config)
log.info('Postgres pool successfully created.')


class PSQLDatabase:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self):
        # getting a connection from the pool
        try:
            self.conn = psql_pool.getconn()
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
            psql_pool.putconn(self.conn)
        except psycopg2.Error as close_error:
            log.error(f'Error while closing the cursor or the connection: {close_error}')

    def commit(self):
        try:
            self.conn.commit()
        except psycopg2.Error as commit_error:
            log.error(f'Error while committing changes to the database: {commit_error}')

    def rollback(self):
        try:
            self.conn.rollback()
        except psycopg2.Error as rollback_error:
            log.error(f'Error while committing changes to the database: {rollback_error}')

    def get_cursor(self):
        return self.cursor

    @staticmethod
    def fetchone_to_dict(cursor):
        row = cursor.fetchone()
        colnames = [desc[0] for desc in cursor.description]
        return dict(zip(colnames, row))

    @staticmethod
    def fetchall_to_dict(cursor):
        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        return [dict(zip(colnames, row)) for row in rows]

    def __enter__(self) -> 'PSQLDatabase':
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


log.info('Creating connection pool for postgres..')
redis_pool = redis.ConnectionPool(**redis_config)
log.info('Postgres pool successfully created.')


class RedisDatabase:
    def __init__(self):
        self.client: Redis = Redis(
            connection_pool = redis_pool,
        )

    def close(self):
        try:
            self.client.close()
        except redis.exceptions.RedisError as close_error:
            log.error(f'Error while closing the redis connection: {close_error}')

    def __enter__(self) -> 'RedisDatabase':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()