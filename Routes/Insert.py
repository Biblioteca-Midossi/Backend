import io
import logging
import os

from fastapi import APIRouter, Request, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from Utils.Database.DbHelper import Database

from PIL import Image

router = APIRouter(
    prefix = '/api',
    tags = ['insert'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)


class InvalidRequestError(Exception):
    pass


class DatabaseError(Exception):
    pass


def check_isbn_exists(isbn: str) -> bool:
    with Database() as db:
        cursor = db.get_cursor()
        cursor.execute('select count(*) from biblioteca.libri where isbn = %s', (isbn,))
        if cursor.fetchone()[0] == 0:
            # print("isbn doesn't exist")
            return False
        else:
            # print("isbn exists")
            return True


def insert_collocazione(collocazione: dict[str, str]) -> int:
    scaffale: str = collocazione.get('scaffale').upper()
    istituto: str = collocazione.get('istituto').upper()

    id_istituto_map: dict = {'ITT': 1, 'LAC': 2, 'LAV': 3}
    id_istituto: int = id_istituto_map.get(istituto)

    with Database() as db:
        cursor = db.get_cursor()

        # check if location is already is in db..
        print('select scaffale 1')
        cursor.execute('select scaffale from biblioteca.collocazioni '
                       'where id_istituto = %i'), (id_istituto,)
        id_collocazione = cursor.fetchone()[0]

        if id_collocazione:
            return id_collocazione
        else:
            try:
                print('insert scaffale 1')
                cursor.execute('insert into biblioteca.collocazioni'
                               '(id_istituto, scaffale) values (%i, %s)',
                               (id_istituto, scaffale)
                               )
                db.commit()

                print('select scaffale 2')
                cursor.execute('select id_collocazione from biblioteca.collocazioni '
                               'where scaffale = %s and id_istituto = %i',
                               (scaffale, id_istituto)
                               )
                return cursor.fetchone()[0]
            except Exception as e:
                raise DatabaseError(e)


def insert_autore(autore: dict[str, str]) -> int:
    nome: str = autore.get('nome')
    cognome: str = autore.get('cognome')

    with Database() as db:
        cursor = db.get_cursor()

        # check if author already exists in db..
        cursor.execute('select id_autore from biblioteca.autori '
                       'where nome = %s and cognome = %s',
                       (nome, cognome)
                       )
        author = cursor.fetchone()[0]

        if author:
            return author
        else:
            cursor.execute('insert into biblioteca.autori '
                           '(nome, cognome) values (%s, %s)',
                           (nome, cognome)
                           )
            db.commit()

            cursor.execute('select id_autore from biblioteca.autori '
                           'where nome = %s and cognome = %s',
                           (nome, cognome)
                           )

            return cursor.fetchone()[0]


def insert_libro(libro, id_autore, id_collocazione):
    isbn: str = libro.get('isbn')
    titolo: str = libro.get('titolo')
    genere: str = libro.get('genere')
    quantita: str = libro.get('quantita')
    casa_editrice: str = libro.get('casa_editrice')
    descrizione: str = libro.get('descrizione')

    print(isbn, titolo, genere, quantita, casa_editrice, descrizione, id_autore, id_collocazione)

    with Database() as db:
        cursor = db.get_cursor()
        print('executing libro..')
        cursor.execute('insert into biblioteca.libri'
                       '(id_collocazione, id_autore, isbn, titolo, '
                       'genere, quantita, casa_editrice, descrizione) '
                       'values (%s, %s, %s, %s, %s, %s, %s, %s)',
                       (id_collocazione, id_autore, isbn, titolo,
                        genere, quantita, casa_editrice, descrizione)
                       )
        print('committing libro..')
        db.commit()


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
        # print(libro.get('isbn'))
        # print('checking isbn..')
        if check_isbn_exists(libro.get('isbn')):
            logging.warning(f"Libro '{libro['titolo']}' non inserito. L'isbn '{libro['isbn']}' esiste gia'.")
            return {"message": "The isbn is already in the database"}, 409
        # print('collocazione...')
        id_collocazione = insert_collocazione(collocazione)
        # print('autore...')
        id_autore = insert_autore(autore)
        # print('libro...')
        insert_libro(libro, id_autore, id_collocazione)
        logging.info(f"Libro '{libro['titolo']}' inserito correttamente nel database.")
        return {"status": "successful"}, 200
    except HTTPException as e:
        raise InvalidRequestError(e.detail)
    except Exception as e:
        logging.error(f"Richiesta invalida: {e}")
        raise DatabaseError(e)


@router.post("/insert")
async def insert(request: Request):
    try:
        data = await request.json()
        for entry in data:
            if entry is not data[9] and entry == '':
                return JSONResponse(
                    {'error': 'Bad request'}, status_code = 400
                )

        # add entry to database
        response = await insert_book_into_database(data)

        return JSONResponse(*response)
    except InvalidRequestError as e:
        logging.error(f"Richiesta invalida: {e}.")
        return JSONResponse({'error': str(e)}, status_code = 400)
    except DatabaseError as e:
        logging.error(f"Qualcosa e' andato storo nel database: {e}.")
        return JSONResponse({'error': str(e)}, status_code = 500)


async def covert_to_png(file_content: bytes):
    try:
        # print('trying to convert')
        with Image.open(io.BytesIO(file_content)) as img:
            # print('converting to rgb')
            img = img.convert('RGB')
            # print('converting to png')
            png_bytes = io.BytesIO()
            img.save(png_bytes, format = 'PNG')
            # print('returning..')
            return png_bytes.getvalue()
    except Exception as e:
        print('exception in png')
        print(e)
        # return JSONResponse({'error': str(e)}, status_code = 500)


@router.post('/thumbnail/{isbn}')
async def upload_thumbnail(isbn: str, file: UploadFile = File(...)):
    try:
        print(isbn)
        # Convert to PNG
        # print('converting to png..')
        png_bytes = await covert_to_png(await file.read())
        # print('file successfully converted!')

        # Make sure the directory is there
        # print('settings save directory..')
        save_directory = './assets/thumbnails/'
        os.makedirs(save_directory, exist_ok = True)

        # Save the uploaded file
        # print('saving..')
        file_path = os.path.join(save_directory, f'{isbn}.png')
        with open(file_path, 'wb') as buffer:
            buffer.write(png_bytes)
        # print('file successfully saved!')

        with Database() as db:
            print('adding thumbnail to database..')
            cursor = db.get_cursor()
            cursor.execute('update biblioteca.libri '
                           'set thumbnail_path = %s where isbn = %s',
                           (file_path[2:], isbn))
            db.commit()

        return JSONResponse({'status': 'successful'}, status_code = 200)

    except DatabaseError as e:
        print('Database error: ', e)
        return JSONResponse({'error': str(e)}, status_code = 500)
    except FileExistsError as e:
        print('FileExistsError:', e)
        raise HTTPException(status_code = 400, detail = "File already exists")
    except IOError as e:
        print('IOERROR:', e)
        raise HTTPException(status_code = 500, detail = str(e))
    except Exception as e:
        print('Unexpected error:', e)
        raise HTTPException(status_code = 500, detail = str(e))
