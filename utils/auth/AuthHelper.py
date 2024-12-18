from logging import getLogger
from typing import Annotated

import bcrypt
from dotenv import get_key
from fastapi import HTTPException, Depends
from fastapi.requests import Request
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from utils.database.DbHelper import PSQLDatabase

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
                cursor.execute('SELECT id_utente, username, id_istituto, ruolo FROM utenti WHERE username = %s', (
                username,))
                return db.fetchone_to_dict(cursor)
        except Exception as e:
            log.error(f"Password verification error: {e}")

    return None


def get_current_user(request: Request):
    session_id = request.cookies.get('session')
    debug(f'session id = {session_id or None}')

    if not session_id:
        raise HTTPException(status_code = 401, detail = "Not authenticated")

    try:
        session_data = decode_session_cookie(session_id)
        debug(session_data)
        if not session_data:
            raise HTTPException(status_code = 401, detail = "Invalid session")
    except Exception as e:
        debug(f'Error decoding session cookie: {e}')
        raise HTTPException(status_code = 401, detail = "Invalid session")

    return session_data


def verify_role(required_roles: list):
    def role_checker(user: Annotated[dict, Depends(get_current_user)]):
        if user['ruolo'] not in required_roles:
            raise HTTPException(status_code = 403, detail = "Insufficient permissions")
        return user
    return role_checker
