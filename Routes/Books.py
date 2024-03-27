from fastapi import APIRouter, Query
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


# def fuzzy_search_author(author_query: str, authors: list[str], threshold = 10):
#     matches = process.extract(author_query, authors, limit = None)
#     return [match[0] for match in matches if match[1] >= threshold]


@router.get('/books')
async def getBooks():
    with Database() as db:
        # gets cursor from db
        cursor = db.get_cursor()
        cursor.execute("select l.titolo, a.nome, a.cognome, l.thumbnail_path "
                       "from biblioteca.libri as l, biblioteca.autori as a "
                       "where l.id_autore = a.id_autore")
        # assigns the result of the query to `raw_books`.
        raw_books: list = cursor.fetchall()
        # print(raw_books)
        # converts raw_books to a list json-like objects.
        books: list[dict] = [
            {
                "titolo": book[0],
                "autore": f"{book[1]} {book[2]}",
                "coverUrl": book[3]
            } for book in raw_books
        ]
    print({'books': raw_books})
    print({'books': books})
    # sends books as a response
    return JSONResponse({'books': books}, status_code = 200)


# @router.get('/books')
# def get_books_by_author(author_query: str = Query(...)):
#     author_names = ["Mark Maggio", "John Smith", "Alice Johnson"]  # Example author names from your database
#     matched_authors = fuzzy_search_author(author_query, author_names)
#
#     return JSONResponse({'matched_authors': matched_authors})


