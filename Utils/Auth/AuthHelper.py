from typing import Annotated

from dotenv import get_key
from fastapi import HTTPException, Depends
from fastapi.requests import Request
from logging import getLogger

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from passlib.context import CryptContext

from Utils.Database.DbHelper import PSQLDatabase

log = getLogger("FileLogger")
debug = log.debug

pwd_context = CryptContext(schemes=['bcrypt'])

# Serializer for cookie handling
serializer = URLSafeTimedSerializer(get_key('.env', 'COOKIE_KEY'))


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
        cursor.execute('select password from utenti '
                       'where username = %s',
                       (username,))
        password_db = cursor.fetchone()[0]
        if password_db and pwd_context.verify(password, password_db):
            cursor.execute('select id_utente, username, id_istituto, ruolo '
                           'from utenti where username = %s', (username,))
            return db.fetchone_to_dict(cursor)
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
