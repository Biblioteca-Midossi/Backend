import logging
# from typing import Optional, Union

import psycopg2.pool
from psycopg2.pool import SimpleConnectionPool
# import redis.exceptions
from redis.asyncio import Redis, ConnectionPool
# from redis.typing import KeyT, ExpiryT, EncodableT, AbsExpiryT, PatternT

from utils.database.db_config import psql_config, redis_config

# from Utils.Database.DatabaseStartupEvent import on_startup

log = logging.getLogger('FileLogger')

# on_startup()
log.info('Creating connection pool for postgres..')
psql_pool = psycopg2.pool.SimpleConnectionPool(maxconn = 4, minconn = 1, **psql_config)
log.info('Postgres pool successfully created.')


class PSQLDatabase:
    def __init__(self):
        self.conn: psycopg2.extensions.connection | None = None
        self.cursor: psycopg2.extensions.cursor | None = None

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
            print(f'Error while committing changes to the database: {commit_error}')
            log.error('Error while committing changes to the database: {commit_error}')

    def rollback(self):
        try:
            self.conn.rollback()
        except psycopg2.Error as rollback_error:
            log.error(f'Error while committing changes to the database: {rollback_error}')

    def get_cursor(self):
        return self.cursor

    def fetchone_to_dict(self) -> dict:
        row = self.cursor.fetchone()
        colnames = [desc[0] for desc in self.cursor.description]
        return dict(zip(colnames, row))

    def fetchall_to_dict(self) -> list[dict]:
        rows = self.cursor.fetchall()
        colnames = [desc[0] for desc in self.cursor.description]
        return [dict(zip(colnames, row)) for row in rows]

    def __enter__(self) -> 'PSQLDatabase':
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


log.info('Creating connection pool for redis..')
redis_pool = ConnectionPool(**redis_config)
log.info('Redis async pool successfully created.')


class RedisDatabase(Redis):
    def __init__(self):
        super().__init__(connection_pool = redis_pool)

    # async def hset(
    #     self,
    #     name: str,
    #     key: Optional[str] = None,
    #     value: Optional[str] = None,
    #     mapping: Optional[dict] = None,
    #     items: Optional[list] = None,
    # ):
    #     return await self.client.hset(name, key, value, mapping, items)
    #
    # async def expire(
    #     self,
    #     name: KeyT,
    #     time: ExpiryT,
    #     nx: bool = False,
    #     xx: bool = False,
    #     gt: bool = False,
    #     lt: bool = False,
    # ):
    #     return await self.client.expire(name, time, nx, xx, gt, lt)
    #
    # async def set(
    #     self,
    #     name: KeyT,
    #     value: EncodableT,
    #     ex: Union[ExpiryT, None] = None,
    #     px: Union[ExpiryT, None] = None,
    #     nx: bool = False,
    #     xx: bool = False,
    #     keepttl: bool = False,
    #     get: bool = False,
    #     exat: Union[AbsExpiryT, None] = None,
    #     pxat: Union[AbsExpiryT, None] = None,
    # ):
    #     return await self.client.set(name, value, ex, px, nx, xx, keepttl, get, exat, pxat)
    #
    # async def keys(self, pattern: PatternT = "*", **kwargs):
    #     return await self.client.keys(pattern, **kwargs)
    #
    # async def hgetall(self, name):
    #     return await self.client.hgetall(name)

    # async def __aenter__(self) -> 'RedisDatabase':
    #     return self
    #
    # async def __aexit__(self, exc_type, exc_val, exc_tb):
    #     await self.aclose()
