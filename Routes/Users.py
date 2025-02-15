import json
import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, Request
from starlette.responses import JSONResponse

from Routes.models.auth_models import UserProfileUpdate
from Routes.services.file_operations import upload_profile_picture
from Routes.services.user_service import get_user_profile, update_user_profile, get_user_by_id
from utils.auth.oauth2 import get_current_user, verify_role, verify_token, create_access_token
from utils.database.db_helper import PSQLDatabase, RedisDatabase

log = logging.getLogger('FileLogger')
debug = log.debug

router = APIRouter(
    prefix = '/users',
    tags = ['users'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)


@router.get('/me')
async def get_profile(auth_data: Annotated[dict, Depends(get_current_user)]):
    user = auth_data["user"]
    new_tokens = auth_data["new_tokens"]

    profile = await get_user_profile(user['id_utente'])
    del profile['password']

    response = JSONResponse(profile, 200)

    if new_tokens:
        response.set_cookie(
            key='access_token',
            value=new_tokens['access_token'],
            httponly=True,
            secure=False,  # TODO: set to True in production
            samesite='strict',
            max_age=7200
        )
        response.set_cookie(
            key='refresh_token',
            value=new_tokens['refresh_token'],
            httponly=True,
            secure=False,  # TODO: set to True in production
            samesite='strict',
            max_age=2592000
        )

    return response


@router.put('/me')
async def update_profile(
    auth_data: Annotated[dict, Depends(get_current_user)],
    profile_update: Optional[UserProfileUpdate] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    user = auth_data['user']
    new_tokens = auth_data['new_tokens']

    try:
        update_data = {}

        # Handle file upload if needed
        if file and file.filename:
            if file.content_type not in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
                raise HTTPException(status_code = 400, detail = "Invalid file type. Only JPEG, JPG, PNG, WEBP and GIF files are allowed")

            if file.size > 5_000_000:   # 5MB
                raise HTTPException(status_code = 400, detail = "File size should not exceed 5MB")

            # Upload new file picture
            await upload_profile_picture(user['id_utente'], file)

            with PSQLDatabase() as db:
                cursor = db.get_cursor()
                cursor.execute('select profile_picture from utenti where id_utente = %s', (user['id_utente'],))
                profile_picture = cursor.fetchone()[0]
            update_data['profile_picture'] = profile_picture

        if profile_update:
            # Convert to dict
            profile_dict = profile_update.model_dump(mode = 'python', exclude_unset = True)
            update_data.update(profile_dict)

        if update_data:
            await update_user_profile(user['id_utente'], update_data)

        response = JSONResponse({'message': 'Profile updated successfully'}, 200)
        if new_tokens:
            response.set_cookie(
                key='access_token',
                value=new_tokens['access_token'],
                httponly=True,
                secure=False,
                samesite='strict',
                max_age=7200
            )
            response.set_cookie(
                key='refresh_token',
                value=new_tokens['refresh_token'],
                httponly=True,
                secure=False,
                samesite='strict',
                max_age=2592000
            )

        return response
    except Exception as e:
        raise HTTPException(status_code = 400, detail=str(e))


@router.get('/get-users', dependencies = [Depends(verify_role(3))])
async def get_users(
        offset: int = Query(default = 0, ge = 0),
        limit: int = Query(default = 10, ge = 1, le = 100)
):
    with PSQLDatabase() as db:
        cursor = db.get_cursor()

        cursor.execute("""
            select count(*) from utenti
        """)
        total_users = cursor.fetchone()[0]

        cursor.execute("""
            select id_utente, nome, cognome, username, ruolo, id_istituto, email
            from utenti
            order by id_utente
            limit %s offset %s
        """, (limit, offset))
        users = db.fetchall_to_dict()

    return JSONResponse(
        {
            "users": users,
            "total": total_users
        },
        200
    )


@router.put('/update-user/{user_id}', dependencies=[Depends(verify_role(3))])
async def update_user(request: Request, auth_data: Annotated[dict, Depends(get_current_user)]):
    user = auth_data["user"]
    new_tokens = auth_data["new_tokens"]

    user_data = (await request.json()).get('user_data')
    user_id = user_data['id_utente']

    try:
        with PSQLDatabase() as db:
            cursor = db.get_cursor()

            cursor.execute("""
                select ruolo
                from utenti
                where id_utente = %s
            """, (user_id,))

            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="User not found")

            target_role = result[0]
            current_user_role = int(user['ruolo'])

            if user_id == user['id_utente'] and 'ruolo' in user_data:
                raise HTTPException(
                    status_code=403,
                    detail="You cannot modify your own role. Please ask someone with a higher role!"
                )

            if target_role >= current_user_role:
                raise HTTPException(
                    status_code=403,
                    detail="Cannot modify users with equal or higher role. Please ask someone with a higher role!"
                )

            if 'ruolo' in user_data and int(user_data['ruolo']) >= current_user_role:
                raise HTTPException(
                    status_code=403,
                    detail="Cannot set role equal to or higher than your own"
                )

            update_fields = []
            values = []

            for key, value in user_data.items():
                if key in ['nome', 'cognome', 'username', 'ruolo', 'email']:
                    update_fields.append(f'{key} = %s')
                    values.append(value)

            if not update_fields:
                raise HTTPException(status_code=400, detail="No valid fields to update")

            values.append(user_id)

            cursor.execute(f"""
                update utenti
                set {', '.join(update_fields)}
                where id_utente = %s
                returning id_utente
            """, tuple(values))

            if not cursor.fetchone()[0]:
                raise HTTPException(status_code=404, detail="User not found")

            db.commit()

            if 'ruolo' in user_data:
                try:
                    async with RedisDatabase() as redis:
                        pattern = f'{user_id}:*'
                        token_keys = await redis.keys(pattern)

                        if token_keys:
                            for key in token_keys:
                                token_data = await redis.get(key)

                                if token_data:
                                    token_info = json.loads(token_data)
                                    token_info['ruolo'] = user_data['ruolo']
                                    await redis.set(key, json.dumps(token_info))

                except Exception as redis_error:
                    print("Redis error:", str(redis_error))
                    return JSONResponse({
                        "message": "User updated successfully but token update failed",
                        "error": str(redis_error)
                    }, 200)

        response = JSONResponse({"message": "User updated successfully"}, 200)

        if new_tokens:
            response.set_cookie(
                key='access_token',
                value=new_tokens['access_token'],
                httponly=True,
                secure=False,
                samesite='strict',
                max_age=7200
            )
            response.set_cookie(
                key='refresh_token',
                value=new_tokens['refresh_token'],
                httponly=True,
                secure=False,
                samesite='strict',
                max_age=2592000
            )

        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
