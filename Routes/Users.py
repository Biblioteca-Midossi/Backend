import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from starlette.responses import JSONResponse

from Routes.models.auth_models import UserProfileUpdate
from Routes.services.file_operations import upload_profile_picture
from Routes.services.user_service import get_user_profile, update_user_profile
from utils.auth.AuthHelper import get_current_user
from utils.database.DbHelper import PSQLDatabase

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
async def get_profile(user: Annotated[dict, Depends(get_current_user)]):
    profile = await get_user_profile(user['id_utente'])
    del profile['password']
    # print(profile)
    return JSONResponse(profile, 200)


@router.put('/me')
async def update_profile(
    user: Annotated[dict, Depends(get_current_user)],
    profile_update: Optional[UserProfileUpdate] = Form(None),
    file: Optional[UploadFile] = File(None)
):
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
                cursor.execute('select profile_picture from users where id = %s', (user['id_utente'],))
                profile_picture = cursor.fetchone()[0]
            update_data['profile_picture'] = profile_picture

        if profile_update:
            # Convert to dict
            profile_dict = profile_update.model_dump(mode = 'python', exclude_unset = True)
            update_data.update(profile_dict)

        if update_data:
            await update_user_profile(user['id_utente'], update_data)

        return JSONResponse({'message': 'Profile updated successfully'}, 200)
    except Exception as e:
        raise HTTPException(status_code = 400, detail=str(e))
