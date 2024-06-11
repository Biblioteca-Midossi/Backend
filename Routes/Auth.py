from dotenv import get_key

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from passlib.context import CryptContext

from pydantic import BaseModel

from redis import Redis

import logging

from typing import Annotated

from Utils.Database.DbHelper import Database


log = logging.getLogger('FileLogger')
debug = log.debug

auth_router = APIRouter(
    prefix = '/auth',
    tags = ['auth'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)

pwd_context = CryptContext(schemes=['bcrypt'])

redis = Redis(host = 'localhost', port = 6379, decode_responses = True, password = get_key('.env', 'REDIS_PASSWORD'))

# Serializer for cookie handling
serializer = URLSafeTimedSerializer(get_key('.env', 'COOKIE_KEY'))


class UserForm(BaseModel):
    nome: str
    cognome: str
    username: str
    email: str
    password: str
    istituto: str | int


class LoginForm(BaseModel):
    username: str
    password: str


def create_session_cookie(data: dict, max_age: int = 14400):
    token = serializer.dumps(data)
    return token


def decode_session_cookie(cookie: str):
    try:
        data = serializer.loads(cookie, max_age = 14400)
        return data
    except (BadSignature, SignatureExpired):
        return None


def verify_user(username: str, password: str):
    with Database() as db:
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


@auth_router.post('/register')
async def register(user: UserForm):
    debug('trying to register..')
    debug(user)
    try:
        with Database() as db:
            cursor = db.get_cursor()
            debug('register select count(*)')
            cursor.execute('select count(*) from utenti '
                           'where username = %s '
                           'or email = %s',
                           (user.username, user.email))
            debug('register if')
            if cursor.fetchone()[0]:
                raise HTTPException(status_code=400, detail="Username already registered or email already used")
            else:
                id_istituto_map: dict = {'EXT': 0, 'ITT': 1, 'LAC': 2, 'LAV': 3}
                id_istituto: int = id_istituto_map.get(user.istituto)

                debug('hashing..')
                hashed_password = pwd_context.hash(user.password)

                debug('register insert..')
                cursor.execute('insert into utenti('
                               'nome, cognome, username, email, password, id_istituto, ruolo)'
                               'values(%s, %s, %s, %s, %s, %s, %s)',
                               (user.nome, user.cognome, user.username, user.email,
                                hashed_password, id_istituto, 0))
                debug('register commit')
                db.commit()
                return JSONResponse({'message': 'You have registered successfully'}, 200)
    except Exception as e:
        db.rollback()
        log.error(f'Error registering user: {str(e)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")


@auth_router.post('/login')
async def login(data: LoginForm):
    username = data.username
    password = data.password
    debug('trying to login..')
    try:
        user = verify_user(username, password)
        debug(user)
        if not user:
            debug('raising ex')
            raise HTTPException(status_code=401, detail="Invalid username or password")
        debug('assigning session_data')
        session_data = {
            'userid': user['id_utente'],
            'username': username,
            'istituto': user['id_istituto'],
            'ruolo': user['ruolo'],
        }
        debug(session_data)
        session_id = create_session_cookie(session_data)
        if not redis.get(session_id):
            debug('Setting session in redis')
            redis.hset(session_id, mapping=session_data)
        
        debug('Setting redis session expiration')
        redis.expire(session_id, 14400)
        debug('Setting session cookie')
        debug(session_id)

        response = JSONResponse({'message': 'Successfully logged in!'}, 200)
        response.set_cookie(
            key='session', 
            value=session_id, 
            httponly=True, 
            samesite='Lax', 
            path='/'
        )
        return response
        
    except Exception as e:
        log.error(f'Error logging in user: {str(e)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")


@auth_router.get('/logout')
async def logout():
    response = JSONResponse({'status': 'successful', 'message': 'Successfully logged out!'}, 200)
    response.delete_cookie('session')
    return response


def get_current_user(request: Request):
    session_id = request.cookies.get('session')
    debug(f'session id = {session_id}')

    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        session_data = decode_session_cookie(session_id)
        if not session_data:
            raise HTTPException(status_code=401, detail="Invalid session")
    except Exception as e:
        debug(f'Error decoding session cookie: {e}')
        raise HTTPException(status_code=401, detail="Invalid session")
    
    return session_data


@auth_router.get('/check')
async def auth_check(user: Annotated[dict, Depends(get_current_user)]):
    debug(user)
    return JSONResponse(
        {
            "userid": user['userid'],
            "username": user['username'],
            "role": user['ruolo']
        }
    )
 