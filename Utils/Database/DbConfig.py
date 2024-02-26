import os
from dotenv import get_key
from typing import Dict, Optional


if os.path.exists('.env'):
    database = get_key('.env', 'DBNAME')
    user = get_key('.env', 'USER')
    password = get_key('.env', 'PASSWORD')
    host = get_key('.env', 'HOST')
    port = get_key('.env', 'PORT')
else:
    # These are specific to our use case, but can be changed.
    database = 'biblioteca'
    user = 'root'
    password = ''
    host = 'localhost'
    port = '3306'


database_config: Dict[str, Optional[str]] = {
    "database": database,
    "user": user,
    "password": password,
    "host": host,
    "port": port,
}
