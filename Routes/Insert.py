import io
import logging
import os

from fastapi import APIRouter, Request, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from Utils.Database.DbHelper import Database

from PIL import Image

router = APIRouter(
    prefix="/api",
    tags=['insert'],
    responses={404: {"description": "Not found"}}
)


class InvalidRequestError(Exception):
    pass


class DatabaseError(Exception):
    pass


def check_isbn_exists(isbn: str) -> bool:
    with Database() as db:
        cursor = db.get_cursor()
        cursor.execute('select count(*) from libri where isbn = %s', (isbn,))
        return cursor.fetchone()[0] > 0


def insert_collocazione(collocazione: dict[str, str]) -> int:
    scaffale: str = collocazione.get('scaffale').upper()
    istituto: str = collocazione.get('istituto').upper()

    id_istituto_map: dict = {'ITT': 1, 'LAC': 2, 'LAV': 3}
    id_istituto: int = id_istituto_map.get(istituto)

    with Database() as db:
        cursor = db.get_cursor()

        cursor.execute('select id_collocazione from collocazioni '
                       'where scaffale = %s and id_istituto = %s',
                       (scaffale, id_istituto))

        id_collocazione = cursor.fetchone()
        if id_collocazione:
            return id_collocazione[0]
        else:
            cursor.execute('insert into collocazioni'
                           '(id_istituto, scaffale) values (%s, %s)',
                           (id_istituto, scaffale))
            db.commit()

            cursor.execute('select id_collocazione from collocazioni '
                           'where scaffale = %s and id_istituto = %s',
                           (scaffale, id_istituto))
            return cursor.fetchone()[0]


def insert_autore(autore: dict[str, str]) -> int:
    nome: str = autore.get('nome')
    cognome: str = autore.get('cognome')

    with Database() as db:
        cursor = db.get_cursor()

        cursor.execute('select id_autore from autori '
                       'where nome = %s and cognome = %s',
                       (nome, cognome))
        author = cursor.fetchone()
        if author:
            return author[0]
        else:
            cursor.execute('insert into autori '
                           '(nome, cognome) values (%s, %s)',
                           (nome, cognome))
            db.commit()

            cursor.execute('select id_autore from autori '
                           'where nome = %s and cognome = %s',
                           (nome, cognome))
            return cursor.fetchone()[0]


def insert_libro(libro, id_autore, id_collocazione):
    isbn: str = libro.get('isbn')
    titolo: str = libro.get('titolo')
    genere: str = libro.get('genere')
    quantita: str = libro.get('quantita')
    casa_editrice: str = libro.get('casa_editrice')
    descrizione: str = libro.get('descrizione')

    with Database() as db:
        cursor = db.get_cursor()

        cursor.execute('insert into libri'
                       '(id_collocazione, id_autore, isbn, titolo, '
                       'genere, quantita, casa_editrice, descrizione) '
                       'values (%s, %s, %s, %s, %s, %s, %s, %s)',
                       (id_collocazione, id_autore, isbn, titolo,
                        genere, quantita, casa_editrice, descrizione))
        db.commit()


async def covert_to_png(file_content: bytes):
    try:
        with Image.open(io.BytesIO(file_content)) as img:
            img = img.convert('RGB')
            png_bytes = io.BytesIO()
            img.save(png_bytes, format='PNG')
            return png_bytes.getvalue()
    except Exception as e:
        logging.error(f"Error converting image to PNG: {e}")
        raise HTTPException(status_code=500, detail="Error converting image to PNG")


@router.post('/thumbnail/{isbn}')
async def upload_thumbnail(isbn: str, file: UploadFile = File(...)):
    try:
        # Convert to PNG
        png_bytes = await covert_to_png(await file.read())

        # Make sure the directory is there
        save_directory = './assets/thumbnails/'
        os.makedirs(save_directory, exist_ok=True)

        # Save the uploaded file
        file_path = os.path.join(save_directory, f'{isbn}.png')
        with open(file_path, 'wb') as buffer:
            buffer.write(png_bytes)

        with Database() as db:
            cursor = db.get_cursor()
            cursor.execute('update libri '
                           'set thumbnail_path = %s where isbn = %s',
                           (file_path[2:], isbn))
            db.commit()

        return JSONResponse({'status': 'successful'}, status_code=200)

    except Exception as e:
        logging.error(f"Error uploading thumbnail: {e}")
        raise HTTPException(status_code=500, detail="Error uploading thumbnail")


async def insert_book_into_database(data: list[str]):
    collocazione = {
        'istituto': data[0],
        'scaffale': data[1],
    }

    autore = {
        'nome': data[2],
        'cognome': data[3],
    }
    libro = {
        'isbn': data[4],
        'titolo': data[5],
        'genere': data[6],
        'quantita': data[7],
        'casa_editrice': data[8],
        'descrizione': data[9],
    }

    try:
        if check_isbn_exists(libro.get('isbn')):
            with Database() as db:
                cursor = db.get_cursor()
                cursor.execute("update libri set quantita = libri.quantita + 1 "
                               "where isbn = %s", (libro.get('isbn'),))
            return {"message": "The Book is already in the database"}, 200

        id_collocazione = insert_collocazione(collocazione)
        id_autore = insert_autore(autore)
        insert_libro(libro, id_autore, id_collocazione)
        logging.info(f"Book '{libro['titolo']}' inserted successfully into the database.")
        return {"status": "successful"}, 200

    except InvalidRequestError as e:
        logging.error(f"Invalid request: {e}.")
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logging.error(f"Database error: {e}.")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")


@router.post("/insert")
async def insert(request: Request):
    try:
        data = await request.json()

        # Check for empty fields
        for entry in data:
            if entry != data[9] and entry == '':
                return JSONResponse({'error': 'Bad request'}, status_code=400)

        # Add entry to database
        response = await insert_book_into_database(data)

        return JSONResponse(*response)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")