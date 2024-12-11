from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

import logging

from typing import Annotated

from Routes.models.auth_models import UserForm, LoginForm
from Routes.services.session_service import create_user_session, delete_user_session
from Routes.services.user_service import check_user_exists, create_user
from utils.auth.AuthHelper import verify_user, get_current_user, hash_password

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


@router.post('/register')
async def register(user: UserForm):
    try:
        log.info('checking user..')
        if check_user_exists(user.username, user.email):
            raise HTTPException(status_code = 400, detail = "Username already registered or email already used")

        hashed_password = hash_password(user.password).decode('utf8')
        print(hashed_password)
        create_user(user, hashed_password)

        return JSONResponse({'message': 'You have registered successfully'}, 201)

    except Exception as e:
        log.error(f'Error registering user: {str(e)}')
        raise HTTPException(status_code = 500, detail = "Internal Server Error")


# THIS ONLY SETS COOKIE WITH SESSION DATA
# TO GET USER DATA, USE /auth/check
@router.post('/login')
async def login(request: Request, data: LoginForm):
    try:
        user = verify_user(data.username, data.password)

        if not user:
            raise HTTPException(status_code = 401, detail = "Invalid username or password")

        session_data = {
            'id_utente': user['id_utente'],
            'username': data.username,
            'istituto': user['id_istituto'],
            'ruolo': user['ruolo'],
        }

        # Remove old session if exists
        old_session_id = request.cookies.get('session')
        if old_session_id:
            delete_user_session(old_session_id)

        # Create new session
        session_id = create_user_session(session_data)

        response = JSONResponse({'message': 'Successfully logged in!'}, 200)
        response.set_cookie(
            key = 'session',
            value = session_id,
            httponly = True,
            samesite = 'lax',
            path = '/'
        )
        return response

    except Exception as e:
        log.error(f'Error logging in user: {str(e)}')
        raise HTTPException(detail = "Internal Server Error", status_code = 500)


@router.get('/logout')
async def logout(request: Request):
    session_id = request.cookies.get('session')

    if session_id:
        delete_user_session(session_id)

    response = JSONResponse({
        'status': 'successful',
        'message': 'Successfully logged out!'
    }, 200)
    response.delete_cookie('session')
    return response


@router.get('/check')
async def auth_check(user: Annotated[dict, Depends(get_current_user)]):
    return JSONResponse(
        {
            **user
        }
    )
