from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse

from Utils.Database.DbHelper import Database
from logging import getLogger

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


@router.get('/')
async def getBooks():
    """
    Get all books from the database.
    
    **Path**: `/books/`
    
    **Method**: `GET`
    
    **Description**:
    Retrieves a list of all books in the database, including their title, author, ID, and cover URL.
    
    **Returns**:
    - JSONResponse: A list of books with status code 200.
    
    **Raises**:
    - HTTPException: If there is an error retrieving the books.
    """
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


@router.get('/{book_id}')
async def getBook(book_id: int = Path(...)):
    """
    Get a specific book by its ID.
    
    **Path**: `/books/{book_id}`
    
    **Method**: `GET`
    
    **Description**:
    Retrieves details of a specific book identified by its ID, including the title, author, ID, description, and cover URL.
    
    **Arguments**:
    - `book_id` (int): The ID of the book to retrieve.
    
    **Returns**:
    - JSONResponse: The book details with status code 200 if found.
    - JSONResponse: Message indicating the book was not found with status code 404.
    
    **Raises**:
    - HTTPException: If there is an error retrieving the book.
    """
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
            log.info(f"Requested book {book_details}")
            print('loggin?')
            return JSONResponse({'book': book_details}, status_code = 200)
        else:
            return JSONResponse({'message': 'Book not found'}, status_code = 404)
