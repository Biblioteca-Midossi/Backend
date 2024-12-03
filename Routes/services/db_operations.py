from logging import getLogger

import psycopg2
from fastapi import HTTPException, UploadFile
from starlette.responses import JSONResponse

from Routes.exceptions import InvalidRequestError
from Routes.services.file_operations import upload_thumbnail
from utils.database.DbHelper import PSQLDatabase

log = getLogger("FileLogger")


def check_isbn_exists(isbn: str) -> bool:
    with PSQLDatabase() as db:
        cursor = db.get_cursor()
        cursor.execute('select count(*) from libri where isbn = %s', (isbn,))
        return cursor.fetchone()[0] > 0


def insert_collocazione(collocazione: dict[str, str]) -> int:
    scaffale: str = collocazione.get('scaffale').upper()
    istituto: str = collocazione.get('istituto').upper()

    id_istituto_map: dict = {'ITT': 1, 'LAC': 2, 'LAV': 3}
    id_istituto: int = id_istituto_map.get(istituto)

    with PSQLDatabase() as db:
        cursor = db.get_cursor()

        cursor.execute('select id_collocazione from collocazioni '
                       'where scaffale = %s and id_istituto = %s',
                       (scaffale, id_istituto))

        id_collocazione = cursor.fetchone()
        if id_collocazione:
            return id_collocazione[0]
        else:
            cursor.execute('insert into collocazioni'
                           '(id_istituto, scaffale) values (%s, %s) '
                           'returning id_collocazione',
                           (id_istituto, scaffale))
            db.commit()
            return cursor.fetchone()[0]


def insert_autore(autore: dict[str, str]) -> int:
    nome: str = autore.get('nome')
    cognome: str = autore.get('cognome')

    with PSQLDatabase() as db:
        cursor = db.get_cursor()

        cursor.execute('select id_autore from autori '
                       'where nome = %s and cognome = %s',
                       (nome, cognome))
        author = cursor.fetchone()
        if author:
            return author[0]
        else:
            cursor.execute('insert into autori '
                           '(nome, cognome) values (%s, %s) '
                           'returning id_autore',
                           (nome, cognome))
            db.commit()
            return cursor.fetchone()[0]  # id_autore


def insert_libro(libro: dict, id_collocazione: int):
    isbn: str = libro.get('isbn')
    titolo: str = libro.get('titolo')
    quantita: str = libro.get('quantita')
    casa_editrice: str = libro.get('casaEditrice')
    descrizione: str = libro.get('descrizione')

    with PSQLDatabase() as db:
        cursor = db.get_cursor()

        cursor.execute('insert into libri'
                       '(id_collocazione, isbn, titolo, '
                       'quantita, casa_editrice, descrizione) '
                       'values (%s, %s, %s, %s, %s, %s) '
                       'returning id_libro',
                       (id_collocazione, isbn, titolo,
                        quantita, casa_editrice, descrizione))
        id_libro = cursor.fetchone()[0]

        # Handle genre insertion
        genres = libro.get('genres', [])
        if not isinstance(genres, list):
            genres = [genres]

        for genre in genres:
            cursor.execute('select id_genere from generi where nome_genere = %s', (genre,))
            existing_genre = cursor.fetchone()

            if not existing_genre:
                # Insert new genre
                cursor.execute('insert into generi (nome_genere) values (%s) returning id_genere', (genre,))
                id_genere = cursor.fetchone()[0]
            else:
                id_genere = existing_genre[0]

            # Associate genre with book
            cursor.execute('insert into libro_generi (id_libro, id_genere) values (%s, %s)', (id_libro, id_genere))

        db.commit()
        return id_libro


def insert_libro_autori(id_libro: int, id_autore: int):
    with PSQLDatabase() as db:
        cursor = db.get_cursor()
        cursor.execute('insert into libro_autori (id_libro, id_autore) values (%s, %s)',
                       (id_libro, id_autore))
        db.commit()


async def insert_book_into_database(data, file: UploadFile):
    collocazione = {
        'istituto': data['istituto'],
        'scaffale': data['scaffale'],
    }

    libro = {
        'isbn': data['isbn'],
        'titolo': data['titolo'],
        'genere': data['genere'],
        'quantita': data['quantita'],
        'casaEditrice': data['casaEditrice'],
        'descrizione': data['descrizione'],
    }

    print(data)

    author_names = [name.strip() for names in data['nomeAutore'] for name in names.split(',')]
    author_surnames = [surname.strip() for surnames in data['cognomeAutore'] for surname in surnames.split(',')]

    if len(author_names) != len(author_surnames):
        raise HTTPException(status_code = 400, detail = "Mismatch between number of names and surnames")

    authors = [{'nome': nome, 'cognome': cognome} for nome, cognome in zip(author_names, author_surnames)]

    print("authors", authors)

    try:
        print('checking isbn')
        if check_isbn_exists(libro.get('isbn')):
            with PSQLDatabase() as db:
                cursor = db.get_cursor()
                cursor.execute("update libri set quantita = libri.quantita + 1 "
                               "where isbn = %s", (libro.get('isbn'),))
                db.commit()
            return JSONResponse(
                {"message": "The Book is already in the database and the inventory has been updated"},
                201
            )

        print('isbn checked')

        id_collocazione = insert_collocazione(collocazione)
        id_libro = insert_libro(libro, id_collocazione)

        for author in authors:
            id_autore = insert_autore(author)
            insert_libro_autori(id_libro, id_autore)
        print('uploading thumbnail')
        await upload_thumbnail(file, id_libro)
        log.info(f"Book '{libro['titolo']}' inserted successfully into the database.")
        return JSONResponse({"status": "successful"}, 201)

    except InvalidRequestError as e:
        log.error(f"Invalid request: {e}.")
        raise HTTPException(status_code = 400, detail = str(e))
    except psycopg2.Error as e:
        log.error(f"database error: {e}.")
        raise HTTPException(status_code = 500, detail = "database error")
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        raise HTTPException(status_code = 500, detail = "Unexpected error")
