from pathlib import Path
import os
from dotenv import load_dotenv, get_key


def get_env(key: str) -> str:
    """
    Returns environment variables from Docker secrets,environment variables, or .env files
    """
    secret_path = Path(f"/run/secrets/{key}")
    if secret_path.exists():
        print('returning from secrets')
        return secret_path.read_text()

    # Fallback to env variables
    value = os.getenv(key)
    if value is not None:
        print('returning from environment')
        return value

    # Fallback to .env file
    print('returning from .env')
    return get_key('.env', key)