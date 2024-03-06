import itertools

from fastapi import APIRouter
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
        cursor = db.get_cursor()
        cursor.execute("select l.titolo, a.nome "
                       "from biblioteca.libri as l, biblioteca.autori as a "
                       "where l.id_autore = a.id_autore")
        raw_books: list = list(itertools.chain(*cursor.fetchall()))
        print(raw_books)

        books: list[dict] = [
            {
                "titolo": book[0],
                "autore": book[1],
            }
            for book in raw_books
        ]
    print({'books': raw_books})
    print({'books': books})
    return JSONResponse({'books': books}, status_code = 200)
