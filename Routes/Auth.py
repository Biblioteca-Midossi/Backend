import secrets

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

import logging

from Routes.models.auth_models import UserForm, TokenRequest
from Routes.services.user_service import check_user_exists, create_user
from utils.auth.auth_helper import verify_user, hash_password
from utils.auth.oauth2 import create_tokens, refresh_access_token, verify_token
from utils.database.db_helper import RedisDatabase


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

async def _set_auth_cookies(response: JSONResponse, tokens: dict, device_id: str):
    """
    Sets authentication cookies on the response object.

    Args:
        response: The JSONResponse object to set cookies on
        tokens: Dictionary containing access_token and refresh_token
        device_id: The device identifier
    """
    # Access token - 2 hours
    response.set_cookie(
        key = 'access_token',
        value = tokens['access_token'],
        httponly = True,
        secure = False,  # TODO: set to True when using HTTPS
        samesite = 'strict',
        max_age = 7200  # 2 hours
    )

    # Refresh token - 30 days
    response.set_cookie(
        key = 'refresh_token',
        value = tokens['refresh_token'],
        httponly = True,
        secure = False,  # TODO: set to True when using HTTPS
        samesite = 'strict',
        max_age = 2592000  # 30 days
    )

    # Device ID - 1 year
    response.set_cookie(
        key = 'device_id',
        value = device_id,
        httponly = True,
        secure = False,  # TODO: set to True when using HTTPS
        samesite = 'strict',
        max_age = 31536000  # 1 year
    )

    return response


@router.get("/token/refresh")
async def refresh_token(request: Request):
    ref_token = request.cookies.get('refresh_token')
    device_id = request.cookies.get('device_id')

    if not ref_token or not device_id:
        raise HTTPException(
            status_code = 401,
            detail = "Missing refresh token or device ID"
        )

    new_tokens = await refresh_access_token(ref_token, device_id)
    if not new_tokens:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid refresh token"
        )

    response = JSONResponse(
        {'message': 'Tokens refreshed successfully'},
        200
    )

    return await _set_auth_cookies(response, new_tokens, device_id)


@router.post('/register')
async def register(user: UserForm):
    try:
        log.info('checking user..')
        if check_user_exists(user.username, str(user.email)):
            raise HTTPException(status_code = 400, detail = "Username already registered or email already used")

        hashed_password = hash_password(user.password).decode('utf8')
        create_user(user, hashed_password)

        return JSONResponse({'message': 'You have registered successfully'}, 201)

    except Exception as e:
        log.error(f'Error registering user: {str(e)}')
        raise HTTPException(status_code = 500, detail = "Internal Server Error")


@router.post('/login')
async def login(credentials: TokenRequest, request: Request):
    try:
        user = verify_user(credentials.username, credentials.password)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        device_id = request.cookies.get('device_id') or secrets.token_urlsafe(16)
        tokens = await create_tokens(user, device_id)

        response = JSONResponse({'message': 'Login successful'}, 200)
        return await _set_auth_cookies(response, tokens, device_id)

    except HTTPException:
        raise
    except Exception as e:
        log.error(f'Error while logging in: {str(e)}')
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get('/logout')
async def logout(request: Request):
    try:
        access_token = request.cookies.get('access_token')
        ref_token = request.cookies.get('refresh_token')
        device_id = request.cookies.get('device_id')

        if access_token and device_id:
            async with RedisDatabase() as redis:
                user_data = await verify_token(access_token)
                if user_data:
                    # Delete all tokens for this device
                    pattern = f"{user_data['id_utente']}:device:{device_id}:*"
                    old_tokens = await redis.keys(pattern)
                    if old_tokens:
                        await redis.delete(*old_tokens)

        response = JSONResponse({
            'status': 'successful',
            'message': 'Successfully logged out!'
        }, 200)

    except Exception as e:
        log.error(f'Error logging out: {e}')
        response = JSONResponse({
            'status': 'error',
            'message': 'Logout failed'
        }, 500)
    finally:
        # Always clear cookies even if redis operations fail
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        response.delete_cookie('device_id')
        return response

@router.get('/check')
async def auth_check(request: Request):
    access_token = request.cookies.get('access_token')
    print('access_token:', access_token)
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    user_data = await verify_token(access_token)
    print("user_data: ", user_data)
    if not user_data:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    return JSONResponse(user_data)
