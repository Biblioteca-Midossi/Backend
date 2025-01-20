import io
import json
import logging
import os
from typing import Annotated

from PIL import Image
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from Routes.models.auth_models import TokenResponse
from utils.auth.oauth2 import get_current_user, verify_role
from utils.database.db_helper import PSQLDatabase

log = logging.getLogger('FileLogger')

router = APIRouter(
    tags = ['test'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)


@router.get('/test')
async def test_route():
    """
    Test Route
    
    **Path**: `/test`
    
    **Method**: `GET`
    
    **Description**:
    This endpoint serves as a basic test to confirm that the API is up and running.
    
    **Returns**:
    - `JSONResponse`: A message confirming that the test route works, with a status code of 200.
    """
    return JSONResponse({'message': 'Test route works! Now try the others! 💀'}, status_code = 200)


@router.get('/get-test')
async def db_get_test():
    """
    database Get Test
    
    **Path**: `/get-test`
    
    **Method**: `GET`
    
    **Description**:
    This endpoint connects to the database, executes a query to fetch all rows from the 'test' table,
    and returns the results in JSON format.
    
    **Returns**:
    - `JSONResponse`: A JSON object containing a list of test results with a status code of 200.
    - `JSONResponse`: A JSON object containing an error message with a status code of 400 if an exception occurs.
    
    **Raises**:
    - `Exception`: If there is an error connecting to the database or executing the query.
    """
    try:
        with PSQLDatabase() as db:
            cursor = db.get_cursor()
            cursor.execute("select * from test")
            test_result = [{
                'test': result[0],
            } for result in cursor.fetchall()]
        return JSONResponse({'result': test_result}, status_code = 200)
    except Exception as e:
        return HTTPException(status_code = 400, detail = f'Error: {e}')


async def covert_to_png(file_content: bytes):
    try:
        with Image.open(io.BytesIO(file_content)) as img:
            img = img.convert('RGB')
            png_bytes = io.BytesIO()
            img.save(png_bytes, format = 'PNG')
            return png_bytes.getvalue()
    except Exception as e:
        log.error(f"Error converting image to PNG: {e}")
        raise HTTPException(status_code = 500, detail = "Error converting image to PNG")


@router.post('/post-test')
async def post_test(request: Request, file: Annotated[UploadFile, File(...)]):
    form_data = await request.form()
    data = json.loads(form_data.get('data'))

    # Convert to PNG
    png_bytes = await covert_to_png(await file.read())

    # Make sure the directory is there
    save_directory = './assets/thumbnails/'
    os.makedirs(save_directory, exist_ok = True)

    # Save the uploaded file
    file_path = os.path.join(save_directory, f'test.png')
    with open(file_path, 'wb') as buffer:
        buffer.write(png_bytes)

    return JSONResponse({'message': 'test successful'}, status_code = 200)


@router.get('/role-test', response_class = TokenResponse, dependencies = [Depends(verify_role(3))])
async def role_test(user: Annotated[dict, Depends(get_current_user)]):
    return JSONResponse(
        {'message': f'User {user['username']} has role {user['ruolo']}'},
        status_code = 200
    )
