from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse

from Utils.Database.DbHelper import Database

router = APIRouter(
    prefix = '/api',
    tags = ['books'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)


@router.get('/books')
async def getBooks():
    with Database() as db:
        # gets cursor from db
        cursor = db.get_cursor()
        cursor.execute("select l.titolo, a.nome, a.cognome, l.id_libro, l.thumbnail_path "
                       "from libri as l, autori as a "
                       "where l.id_autore = a.id_autore")
        # assigns the result of the query to `raw_books`.
        raw_books: list = cursor.fetchall()

        # converts `raw_books` to a list json-like objects.
        books: list[dict] = [
            {
                "titolo": book[0],
                "autore": f"{book[1]} {book[2]}",
                "id": f"{book[3]}",
                "coverUrl": book[4]
            } for book in raw_books
        ]
    return JSONResponse({'books': books}, status_code = 200)


@router.get('/books/{book_id}')
async def getBook(book_id: int = Path(...)):
    with Database() as db:
        cursor = db.get_cursor()
        cursor.execute("SELECT l.titolo, a.nome, a.cognome, l.id_libro, l.descrizione, "
                       "l.thumbnail_path "
                       "FROM libri as l, autori as a "
                       "WHERE l.id_autore = a.id_autore AND l.id_libro = %s", (book_id,))
        book = cursor.fetchone()

        if book:
            book_details = {
                "titolo": book[0],
                "autore": f"{book[1]} {book[2]}",
                "id": f"{book[3]}",
                "descrizione": book[4],
                "coverUrl": book[5]
            }
            return JSONResponse({'book': book_details}, status_code = 200)
        else:
            return JSONResponse({'message': 'Book not found'}, status_code = 404)
