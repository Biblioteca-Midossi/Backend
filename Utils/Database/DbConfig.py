import logging
import os
from dotenv import get_key
from typing import Dict, Optional


log = logging.getLogger('FileLogger')

if os.path.exists('.env'):
    try:
        database = get_key('.env', 'DBNAME')
        user = get_key('.env', 'USER')
        password = get_key('.env', 'PASSWORD')
        host = get_key('.env', 'HOST')
        port = get_key('.env', 'PORT')
        options = f"-c search_path={get_key('.env', 'SCHEMA')}"
    except Exception:
        log.error("Your .env is not complete. Try checking for missing fields")
        raise Exception("Your .env is not complete. Try checking for missing fields")
else:
    log.error("No .env found at project root")
    raise Exception("No .env found at project root")

database_config: Dict[str, Optional[str]] = {
    "database": database,
    "user": user,
    "password": password,
    "host": host,
    "port": port,
    "options": options,
}
