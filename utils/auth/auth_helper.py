from logging import getLogger

import bcrypt
from dotenv import get_key
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from utils.database.db_helper import PSQLDatabase

log = getLogger("FileLogger")
debug = log.debug

# Serializer for cookie handling
serializer = URLSafeTimedSerializer(get_key('.env', 'COOKIE_KEY'))


def hash_password(password: str):
    return bcrypt.hashpw(password = password.encode('utf-8'), salt = bcrypt.gensalt())


def verify_password(plain_password: str, hashed_password: str):
    # debug(f"{plain_password.encode('utf-8')}, {hashed_password}" )
    return bcrypt.checkpw(
        password = plain_password.encode('utf-8'),
        hashed_password = hashed_password.encode('utf-8')
    )


def create_session_cookie(data: dict):
    cookie = serializer.dumps(data)
    return cookie


def decode_session_cookie(cookie: str):
    try:
        data = serializer.loads(cookie, max_age = 14400)
        return data
    except (BadSignature, SignatureExpired):
        return None


def verify_user(username: str, password: str):
    with PSQLDatabase() as db:
        cursor = db.get_cursor()

        # First, check if user exists
        cursor.execute('SELECT password FROM utenti WHERE username = %s', (username,))
        stored_password = cursor.fetchone()[0]

        if not stored_password:
            log.error(f"User {username} not found")
            return None

        try:
            if verify_password(password, stored_password):
                cursor.execute("""
                    SELECT id_utente, username, id_istituto, ruolo
                    FROM utenti
                    WHERE username = %s
                """, (username,))
                return db.fetchone_to_dict()
        except Exception as e:
            log.error(f"Password verification error: {e}")

    return None

async def get_foo_user():
    """Dummy admin user for no_login_mode"""
    return {
        'id_utente': 0,
        'username': 'foo',
        'ruolo': 4,
        'id_istituto': 0
    }
