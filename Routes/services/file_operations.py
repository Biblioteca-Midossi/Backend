import io
import os
from logging import getLogger

from PIL import Image
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from utils.database.db_helper import PSQLDatabase

log = getLogger("FileLogger")


async def convert_to_png(file_content: bytes):
    try:
        with Image.open(io.BytesIO(file_content)) as img:
            img = img.convert('RGB')
            png_bytes = io.BytesIO()
            img.save(png_bytes, format = 'PNG')
            return png_bytes.getvalue()
    except Exception as e:
        log.error(f"Error converting image to PNG: {e}")
        raise HTTPException(status_code = 500, detail = "Error converting image to PNG")


async def upload_thumbnail(file, book_id):
    try:
        # Convert to PNG
        png_bytes = await convert_to_png(await file.read())

        # Make sure the directory is there
        save_directory = './assets/thumbnails/'
        os.makedirs(save_directory, exist_ok = True)

        # Save the uploaded file
        file_path = os.path.join(save_directory, f'{book_id}.png')
        with open(file_path, 'wb') as buffer:
            buffer.write(png_bytes)

        with PSQLDatabase() as db:
            cursor = db.get_cursor()
            cursor.execute('update libri '
                           'set thumbnail_path = %s where id_libro = %s',
                           (file_path[2:], book_id))
            db.commit()

        return JSONResponse({'status': 'successful'}, status_code = 200)

    except Exception as e:
        log.error(f"Error uploading thumbnail: {e}")
        raise HTTPException(status_code = 500, detail = "Error uploading thumbnail")


async def upload_profile_picture(file, user_id):
    try:
        # Convert to PNG
        png_bytes = await convert_to_png(await file.read())

        # Make sure the directory is there
        save_directory = './assets/profile_pictures/'
        os.makedirs(save_directory, exist_ok = True)

        # Save the uploaded file
        file_path = os.path.join(save_directory, f'{user_id}.png')
        with open(file_path, 'wb') as buffer:
            buffer.write(png_bytes)

        with PSQLDatabase() as db:
            cursor = db.get_cursor()
            cursor.execute('update utenti '
                           'set profile_picture = %s where id_utente = %s',
                           (file_path[2:], user_id))
            db.commit()

        return JSONResponse({'status': 'successful'}, status_code = 200)

    except Exception as e:
        log.error(f"Error uploading profile picture: {e}")
        raise HTTPException(status_code = 500, detail = "Error uploading profile picture")
