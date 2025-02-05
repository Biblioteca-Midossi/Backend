from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    UploadFile,
    File,
    Depends,
    Query
)
from fastapi.requests import Request
from fastapi.responses import JSONResponse

import json

from logging import getLogger

import os

import psycopg2

from typing import Annotated

from Routes.services.db_operations import insert_book_into_database
from Routes.services.file_operations import convert_to_png
from utils.auth.oauth2 import verify_role
from utils.database.db_helper import PSQLDatabase

log = getLogger("FileLogger")

router = APIRouter(
    prefix = '/books',
    tags = ['books'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)


@router.get('')
async def get_books(
        page: int = Query(1, alias = 'page'),
        limit: int = Query(12, alias = 'limit'),
        search: str = Query(None, alias = 'search')
):
    offset = (page - 1) * limit
    with PSQLDatabase() as db:
        cursor = db.get_cursor()
        if search:
            cursor.execute("""
                SELECT l.id_libro, l.titolo, l.thumbnail_path, l.isbn, l.quantita,
                       l.casa_editrice, l.descrizione, i.id_istituto, c.scaffale,
                       ARRAY_AGG(DISTINCT g.nome_genere) as generi,
                       COUNT(*) OVER () as total_count,
                       CEIL(COUNT(*) OVER () *1.0 / %s)::int as maxpage
                FROM libri l
                LEFT JOIN collocazioni c ON l.id_collocazione = c.id_collocazione
                LEFT JOIN istituti i ON c.id_istituto = i.id_istituto
                LEFT JOIN libro_autori la ON l.id_libro = la.id_libro
                LEFT JOIN autori a ON la.id_autore = a.id_autore
                LEFT JOIN libro_generi lg ON l.id_libro = lg.id_libro
                LEFT JOIN generi g ON lg.id_genere = g.id_genere
                WHERE l.titolo ilike %s 
                    OR a.nome ilike %s
                    OR a.cognome ilike %s
                    OR g.nome_genere ilike %s
                GROUP BY l.id_libro, i.id_istituto, c.scaffale
                ORDER BY l.id_libro
                LIMIT %s OFFSET %s
            """, (limit, f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%', limit, offset)
            )
        else:
            cursor.execute("""
                SELECT l.id_libro, l.titolo, l.thumbnail_path, l.isbn, 
                       l.quantita, l.casa_editrice, l.descrizione,
                       i.id_istituto, c.scaffale,
                       ARRAY_AGG(DISTINCT g.nome_genere) AS generi,
                       COUNT(*) OVER () AS total_count,
                       CEIL(COUNT(*) OVER () * 1.0 / %s)::int AS maxpage 
                FROM libri l
                LEFT JOIN collocazioni c ON l.id_collocazione = c.id_collocazione
                LEFT JOIN istituti i ON c.id_istituto = i.id_istituto
                LEFT JOIN libro_generi lg ON l.id_libro = lg.id_libro
                LEFT JOIN generi g ON lg.id_genere = g.id_genere
                GROUP BY l.id_libro, i.id_istituto, c.scaffale
                ORDER BY l.id_libro
                LIMIT %s OFFSET %s
            """, (limit, limit, offset)
            )

        raw_books: list = db.fetchall_to_dict()

        if not raw_books:
            raise HTTPException(404, 'Books not found')

        books = []
        for book in raw_books:
            # Fetch authors for each book
            cursor.execute("""
                SELECT a.nome, a.cognome 
                FROM libro_autori la, autori a
                WHERE la.id_autore = a.id_autore
                    AND la.id_libro = %s
                """, (book['id_libro'],)
            )
            authors = [f"{author['nome']} {author['cognome']}" for author in db.fetchall_to_dict()]
            books.append({
                "titolo": book['titolo'],
                "autori": authors,
                "id": book['id_libro'],
                "coverUrl": book['thumbnail_path'],
                "isbn": book['isbn'],
                "genere": book['generi'],
                "quantita": book['quantita'],
                "casaEditrice": book['casa_editrice'],
                "descrizione": book['descrizione'],
                "istituto": book['id_istituto'],
                "scaffale": book['scaffale'],
            })

        maxpage = int(raw_books[0]['maxpage']) if raw_books else 1

    return JSONResponse({'books': books, 'maxpage': maxpage}, 200)


@router.get('/{book_id}')
async def get_book(book_id: int = Path(...)):
    """
    Get a specific book by its ID.

    **Path**: `/books/{book_id}`

    **Method**: `GET`

    **Description**:
    Retrieves details of a specific book identified by its ID, including the title, authors, description, and cover URL.

    **Arguments**:
    - `book_id` (int): The ID of the book to retrieve.

    **Returns**:
    - JSONResponse: The book details with status code 200 if found.
    - JSONResponse: Message indicating the book was not found with status code 404.

    **Raises**:
    - HTTPException: If an error occurs while retrieving the book.
    """
    with PSQLDatabase() as db:
        cursor = db.get_cursor()

        # Fetch book details
        cursor.execute("""
            SELECT l.*, c.id_istituto, c.scaffale, ARRAY_AGG(DISTINCT g.nome_genere) as generi
            FROM libri l, collocazioni c, libro_generi lg, generi g
            WHERE l.id_collocazione = c.id_collocazione
                AND l.id_libro = lg.id_libro
                AND lg.id_genere = g.id_genere
                AND l.id_libro = %s
            GROUP BY l.id_libro, c.id_istituto, c.scaffale
            """, (book_id,)
        )

        book = db.fetchone_to_dict()

        if not book:
            raise HTTPException(404, 'Book not found')

        # Fetch authors for the book
        cursor.execute(
            """
            SELECT a.nome, a.cognome
            FROM libro_autori la, autori a
            WHERE la.id_autore = a.id_autore
                AND la.id_libro = %s
            """,
            (book_id,)
        )
        authors = [f"{author['nome']} {author['cognome']}" for author in db.fetchall_to_dict()]

        # Construct response
        book_details = {
            "isbn": book['isbn'],
            "titolo": book['titolo'],
            "genere": book['generi'],
            "quantita": book['quantita'],
            "casaEditrice": book['casa_editrice'],
            "descrizione": book['descrizione'],
            "autori": authors,
            "coverUrl": book['thumbnail_path'],
            "id": book_id,
            "istituto": book['id_istituto'],
            "scaffale": book['scaffale'],
        }

        log.info(f"Requested book {book_details}")
        return JSONResponse({'book': book_details}, 200)


@router.post('', dependencies = [Depends(verify_role(3))])
async def create_book(data: Request, thumbnail: UploadFile = File(None)):
    """
    Insert a new book into the database via a JSON request.

    **Path**: `/books/`

    **Method**: `POST`

    **Description**:
    Receives a JSON request containing book details and inserts the book into the database. If the book already exists, it updates the quantity.

    **Arguments**:
    - `data` (Request): The request object containing the JSON payload (information about the book).
    - `thumbnail` (Annotated[UploadFile, File(...)]): The file attached to the FormData (the book's thumbnail).

    **Returns**:
    - JSONResponse: Status message indicating success or failure.

    **Raises**:
    - HTTPException: If an unexpected error occures.
    """
    try:
        form_data = await data.form()
        data_str = form_data.get('data')
        log.debug(data_str)

        if not data_str:
            raise HTTPException(status_code = 400, detail = "Missing data in the form")

        data = json.loads(data_str)
        # if len(data) != 10:
        #    raise HTTPException(status_code = 400, detail = "Data list is not complete")

        # Add entry to database
        response: JSONResponse = await insert_book_into_database(data, thumbnail)
        return response

    except Exception as e:
        log.error(f"Unexpected error: {e}")
        raise HTTPException(status_code = 500, detail = "Unexpected error")


@router.put("/{book_id}", dependencies = [Depends(verify_role(3))])
async def update_book(updated_book: Request, file: Annotated[UploadFile, File(...)] = None, book_id: int = Path(...)):
    """
    Update a book in the database.

    **Path**: `/books/`

    **Method**: `PUT`

    **Description**:
    Updates book details in the database, optionally updating the thumbnail.

    **Arguments**:
    - `request` (Request): The request object containing the JSON payload.
    - `file` (UploadFile, optional): The new thumbnail file.
    - `book_id` (int): The ID of the book to update.

    **Returns**:
    - JSONResponse: Message indicating successful update.

    **Raises**:
    - HTTPException: If the book is not found or cannot be updated.
    """

    try:
        form_data = await updated_book.form()
        data_str = form_data.get('updatedBook')

        if not data_str:
            raise HTTPException(status_code = 400, detail = "Missing data in the form")

        data = json.loads(data_str)

        with PSQLDatabase() as db:
            cursor = db.get_cursor()

            # Check if book exists
            cursor.execute('select * from libri where id_libro = %s', (book_id,))
            book = db.fetchone_to_dict()

            if not book:
                raise HTTPException(404, 'Book not found')

            update_fields = {}
            if 'isbn' in data:
                update_fields['isbn'] = data['isbn']
            if 'titolo' in data:
                update_fields['titolo'] = data['titolo']
            if 'quantita' in data:
                update_fields['quantita'] = data['quantita']
            if 'casaEditrice' in data:
                update_fields['casa_editrice'] = data['casaEditrice']
            if 'descrizione' in data:
                update_fields['descrizione'] = data['descrizione']

            # update genre(s)
            # When updating a book
            if 'genere' in data:
                # Remove existing genre associations
                cursor.execute('DELETE FROM libro_generi WHERE id_libro = %s', (book_id,))

                # Ensure genres is a list
                genres = data['genere'] if isinstance(data['genere'], list) else [data['genere']]

                for genre in genres:
                    # Find or insert genre
                    cursor.execute('SELECT id_genere FROM generi WHERE nome_genere = %s', (genre,))
                    existing_genre = cursor.fetchone()

                    if not existing_genre:
                        # Insert new genre if it doesn't exist
                        cursor.execute('INSERT INTO generi (nome_genere) VALUES (%s) RETURNING id_genere', (genre,))
                        id_genere = cursor.fetchone()[0]
                    else:
                        id_genere = existing_genre[0]

                    # Associate genre with book
                    cursor.execute('INSERT INTO libro_generi (id_libro, id_genere) VALUES (%s, %s)', (
                        book_id, id_genere))

            # update author(s) if provided
            if 'nomeAutore' in data and 'cognomeAutore' in data:
                cursor.execute('delete from libro_autori where id_libro = %s', (book_id,))

                # add new author associations
                author_names = [name.strip() for name in data['nomeAutore']]
                author_surnames = [surname.strip() for surname in data['cognomeAutore']]

                if len(author_names) != len(author_surnames):
                    raise HTTPException(status_code = 400, detail = "Mismatch between number of names and surnames")

                processed_authors = set()  # To prevent duplicate associations

                for nome, cognome in zip(author_names, author_surnames):
                    # Find or insert author
                    cursor.execute('SELECT id_autore FROM autori WHERE nome = %s AND cognome = %s', (nome, cognome))
                    author = cursor.fetchone()

                    if not author:
                        # Insert new author if not exists
                        cursor.execute('INSERT INTO autori (nome, cognome) VALUES (%s, %s) RETURNING id_autore', (
                            nome, cognome))
                        id_autore = cursor.fetchone()[0]
                    else:
                        id_autore = author[0]

                    # Prevent duplicate author associations
                    if (book_id, id_autore) not in processed_authors:
                        cursor.execute(
                            'INSERT INTO libro_autori(id_libro, id_autore) VALUES (%s, %s) ON CONFLICT DO NOTHING',
                            (book_id, id_autore)
                        )
                        processed_authors.add((book_id, id_autore))

            # Construct and execute update query
            if update_fields:
                set_clause = ', '.join([f"{k} = %s" for k in update_fields.keys()])
                query = f'UPDATE libri SET {set_clause} WHERE id_libro = %s'
                values = list(update_fields.values()) + [book_id]

                cursor.execute(query, values)

            if file and file.filename:
                save_directory = './assets/thumbnails/'
                existing_file_path = os.path.join(save_directory, f'{book_id}.png')

                # Delete existing file if it exists
                if os.path.exists(existing_file_path):
                    try:
                        os.remove(existing_file_path)
                        log.info(f"Deleted existing thumbnail for book {book_id}")
                    except Exception as e:
                        log.error(f"Error deleting existing thumbnail: {e}")

                png_bytes = await convert_to_png(await file.read())
                os.makedirs(save_directory, exist_ok = True)
                file_path = os.path.join(save_directory, f'{book_id}.png')

                with open(file_path, 'wb') as buffer:
                    buffer.write(png_bytes)

                cursor.execute('update libri set thumbnail_path = %s where id_libro = %s',
                               (file_path[2:], book_id))

            db.commit()
            log.info(f'Book with ID {book_id} updated successfully')
            return JSONResponse({'message': 'Book updated successfully'}, 200)
    except psycopg2.Error as e:
        log.error(f"database error druing book update: {e}")
        raise HTTPException(status_code = 400, detail = f"database error during book update: {e}")
    except Exception as e:
        log.error(f"Unexpected error during book update: {e}")
        raise HTTPException(status_code = 500, detail = f"Unexpected error during book update: {e}")


@router.delete("/{book_id}", dependencies = [Depends(verify_role(3))])
async def delete_book(book_id: int = Path(...)):
    """
    Delete a book from the database.

    **Path**: `/books/{book_id}`

    **Method**: `DELETE`

    **Description**:
    Deletes a specific book identified by its ID from the database.
    Removes associated entries in libro_autori and deletes the book's thumbnail.

    **Arguments**:
    - `book_id` (int): The ID of the book to delete.

    **Returns**:
    - JSONResponse: Message indicating successful deletion.

    **Raises**:
    - HTTPException: If the book is not found or cannot be deleted.
    """
    try:
        with PSQLDatabase() as db:
            cursor = db.get_cursor()

            # check if book exists
            cursor.execute('select * from libri where id_libro = %s', (book_id,))
            book = db.fetchone_to_dict()

            if not book:
                raise HTTPException(404, 'Book not found')

            # Delete thumbnail file if it exists
            thumbnail_path = book['thumbnail_path']
            if thumbnail_path:
                try:
                    os.remove(f"./{thumbnail_path}")
                except FileNotFoundError:
                    log.warning(f'Thumbnail file not found: {thumbnail_path}')

            # Delete libro_autori entries first
            cursor.execute('delete from libro_autori where id_libro = %s', (book_id,))

            # Delete book
            cursor.execute('delete from libri where id_libro = %s', (book_id,))
            db.commit()

            log.info(f'Book with ID {book_id} deleted successfully')
            return JSONResponse({'message': 'Libro eliminato con successo'}, status_code = 200)
    except psycopg2.Error as e:
        log.error(f"database error during book deletion: {e}")
        raise HTTPException(status_code = 500, detail = f"database error during book deletion: {e}")
    except Exception as e:
        log.error(f"Unexpected error during book deletion: {e}")
        raise HTTPException(status_code = 500, detail = f"Unexpected error during book deletion: {e}")
