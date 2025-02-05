import logging
import os
from typing import Dict, Optional

from utils.env import get_env

log = logging.getLogger('FileLogger')

if os.path.exists('.env'):
    try:
        host = get_env( 'HOST')

        psql_database = get_env('DBNAME')
        psql_user = get_env('USER')
        psql_password = get_env('PASSWORD')
        psql_port = get_env('PORT')
        psql_options = f"-c search_path={get_env('SCHEMA')}"

        redis_port = get_env('REDIS_PORT')
        redis_password = get_env('REDIS_PASSWORD')

    except Exception:
        log.error("Your .env is not complete. Try checking for missing fields")
        raise Exception("Your .env is not complete. Try checking for missing fields")
else:
    log.error("No .env found at project root")
    raise Exception("No .env found at project root")

psql_config: Dict[str, Optional[str]] = {
    "database": psql_database,
    "user": psql_user,
    "password": psql_password,
    "host": host,
    "port": psql_port,
    "options": psql_options,
}

redis_config: Dict[str, Optional[str]] = {
    "host": host,
    "port": redis_port,
    "password": redis_password,
    "decode_responses": True,
    "protocol": 3,
}
