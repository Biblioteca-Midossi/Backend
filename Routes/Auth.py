from dotenv import get_key

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from redis import Redis

import logging

from typing import Annotated

from Utils.Auth.AuthHelper import pwd_context, verify_user, create_session_cookie, get_current_user
from Utils.Database.DbHelper import Database


log = logging.getLogger('FileLogger')
debug = log.debug

router = APIRouter(
    prefix = '/auth',
    tags = ['auth'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)

redis = Redis(host = get_key('.env', 'HOST'), port = 6379, decode_responses = True, password = get_key('.env', 'REDIS_PASSWORD'))


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


@router.post('/register')
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


@router.post('/login')
async def login(request: Request, data: LoginForm):
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
        debug(session_id)

        old_session_id = request.cookies.get('session')
        if old_session_id and redis.exists(old_session_id):
            debug('deleting old session')
            redis.delete(old_session_id)

        if not redis.exists(session_id):
            debug('Setting session in redis')
            redis.hset(session_id, mapping = session_data)
        
        debug('Setting redis session expiration')
        redis.expire(session_id, 14400)

        debug('Setting session cookie')
        response = JSONResponse({'message': 'Successfully logged in!'}, 200)
        response.set_cookie(
            key='session', 
            value=session_id, 
            httponly=True, 
            samesite='lax',
            path='/'
        )
        return response
        
    except Exception as e:
        log.error(f'Error logging in user: {str(e)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get('/logout')
async def logout(request: Request):
    session_id = request.cookies.get('session')
    debug(f'Logging out session {session_id}')

    if session_id:
        redis.delete(session_id)
        debug(f'Session {session_id} deleted from Redis')

    response = JSONResponse({'status': 'successful', 'message': 'Successfully logged out!'}, 200)
    response.delete_cookie('session')
    return response


@router.get('/check')
async def auth_check(user: Annotated[dict, Depends(get_current_user)]):
    debug(user)
    return JSONResponse(
        {
            "userid": user['userid'],
            "username": user['username'],
            "role": user['ruolo']
        }
    )
 