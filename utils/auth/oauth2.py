import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, Request

from Routes.services.user_service import get_user_by_id
from utils.auth.auth_helper import get_foo_user
from utils.database.db_helper import RedisDatabase
from utils.env import get_env

ACCESS_TOKEN_EXPIRE = 7200  # 2 hours
REFRESH_TOKEN_EXPIRE = 2592000  # 30 days


async def get_current_user(request: Request):
    if bool(get_env('NO_LOGIN_MODE')):
        return get_foo_user()

    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    device_id = request.cookies.get('device_id')

    if not device_id:
        raise HTTPException(status_code=401, detail="Missing device ID")

    user_data = None
    new_tokens = None

    if access_token:
        user_data = await verify_token(access_token, device_id)

    if not user_data and refresh_token:
        new_tokens = await refresh_access_token(refresh_token, device_id)
        if new_tokens:
            user_data = await verify_token(new_tokens['access_token'], device_id)

    if not user_data:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {"user": user_data, "new_tokens": new_tokens}


def verify_role(required_role: int):
    def role_checker(auth_data: Annotated[dict, Depends(get_current_user)]):
        user = auth_data['user']
        if int(user['ruolo']) < required_role:
            raise HTTPException(status_code = 403, detail = "Insufficient permissions")
        return auth_data

    return role_checker


async def create_access_token(user_data: dict, device_id: str):
    access_token = secrets.token_urlsafe(32)
    user_id = user_data['id_utente']

    token_data = {
        "id_utente": user_id,
        "username" : user_data['username'],
        "ruolo": user_data['ruolo'],
        "device_id" : device_id
    }

    async with RedisDatabase() as redis:
        async with redis.pipeline() as pipe:
            old_access_tk = await redis.keys(f'{user_id}:device:{device_id}:access:*')
            if old_access_tk:
                await pipe.delete(*old_access_tk)

            await pipe.hset(f'{user_id}:device:{device_id}:access:{access_token}', mapping=token_data)
            await pipe.expire(f'{user_id}:device:{device_id}:access:{access_token}', ACCESS_TOKEN_EXPIRE)
            await pipe.execute()

    return access_token


async def create_tokens(user_data: dict, device_id: str):
    access_token = secrets.token_urlsafe(32)
    refresh_token = secrets.token_urlsafe(32)
    user_id = user_data['id_utente']

    token_data = {
        "id_utente": user_id,
        "username": user_data["username"],
        "ruolo": user_data["ruolo"],
        "device_id": device_id
    }

    async with RedisDatabase() as redis:
        async with redis.pipeline() as pipe:
            # try to delete old user-device tokens
            old_tokens = await redis.keys(f'{user_id}:device{device_id}:*')
            if old_tokens:
                await pipe.delete(*old_tokens)

            # store in redis and set expiration
            await pipe.hset(f'{user_id}:device:{device_id}:access:{access_token}', mapping = token_data)
            await pipe.expire(f'{user_id}:device:{device_id}:access:{access_token}', ACCESS_TOKEN_EXPIRE)

            await pipe.set(
                f"{user_id}:device:{device_id}:refresh:{refresh_token}",
                user_data['id_utente'],
                ex = REFRESH_TOKEN_EXPIRE
            )

            await pipe.execute()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "device_id": device_id,
    }


async def verify_token(token: str, device_id: str = None):
    pattern = f'*:access:{token}' if not device_id else f'*:device:{device_id}:access:{token}'
    async with RedisDatabase() as redis:
        token_key = await redis.keys(pattern)
        if not token_key:
            return None

        user_data = await redis.hgetall(token_key[0])
        if device_id and user_data.get('device_id') != device_id:
            return None

        user_data['id_utente'], user_data['ruolo'] = int(user_data['id_utente']), int(user_data['ruolo'])
        return user_data


async def refresh_access_token(refresh_token: str, device_id: str):
    async with RedisDatabase() as redis:
        token_key = await redis.keys(f'*:device:{device_id}:refresh:{refresh_token}')
        if not token_key:
            return None

        user_id = await redis.get(token_key[0])
        if not user_id:
            return None

        user_data = await get_user_by_id(user_id)
        return {
            "access_token": await create_access_token(user_data, device_id),
            "refresh_token": refresh_token
        }
