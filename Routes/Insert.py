import mysql.connector
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from Utils.Database.DbHelper import Database

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


def insert_collocazione(collocazione: dict[str, str]) -> int:
    scaffale: str = collocazione.get('scaffale').upper()
    istituto: str = collocazione.get('istituto')
    print('isnan check')
    try:
        print('isnan check')
        if not istituto.isdigit():
            print('opening database...')
            with Database() as db:
                cursor = db.get_cursor()
                match istituto.upper():
                    case 'ITT':
                        print('case itt')
                        id_istituto = 1
                    case 'LAC':
                        print('case lac')
                        id_istituto = 2
                    case 'LAV':
                        print('case lav')
                        id_istituto = 3
                    case _:
                        print('case _')
                        raise HTTPException(
                            status_code=400,
                            detail='Bad request. Check `Istituto`'
                        )

                print('first ex')
                cursor.execute('insert into biblioteca.collocazioni'
                               '(id_istituto, scaffale) values (%s, %s)',
                               (id_istituto, scaffale)
                               )
                print('commit')
                db.commit()

                print('second ex')
                cursor.execute('select id_collocazione from biblioteca.collocazioni '
                               'where scaffale = %s and id_istituto = %s',
                               (scaffale, id_istituto)
                               )
                print('fetch')
                return cursor.fetchone()[0]
    except mysql.connector.Error as e:
        print(e)


def insert_autore(autore: dict[str, str]):
    nome: str = autore.get('nome')
    cognome: str = autore.get('cognome')

    with Database() as db:
        cursor = db.get_cursor()
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

    with Database() as db:
        cursor = db.get_cursor()
        cursor.execute('insert into biblioteca.libri'
                       '(id_collocazione, id_autore, isbn, titolo, '
                       'genere, quantita, casa_editrice, descrizione) '
                       'values (%s, %s, %s, %s, %s, %s, %s, %s)',
                       (id_collocazione, id_autore, isbn, titolo,
                        genere, quantita, casa_editrice, descrizione)
                       )


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
        print('collocazione...')
        id_collocazione = insert_collocazione(collocazione)
        print('autore...')
        id_autore = insert_autore(autore)
        print('libro...')
        insert_libro(libro, id_autore, id_collocazione)
        print('returning 200...')
        return {"status": "successful"}, 200
    except HTTPException as e:
        raise InvalidRequestError(e.detail)
    except Exception as e:
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
        return JSONResponse({'error': str(e)}, status_code = 400)
    except DatabaseError as e:
        return JSONResponse({'error': str(e)}, status_code=500)