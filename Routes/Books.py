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
    raw_books = [
        {
            'titolo': 'Dante',
            'autore': 'Alessandro',
            'coverUrl': 'https://blogs.youcanprint.it/wp-content/uploads/2022/05/61xSNpivMML.jpeg'
        }
    ]
    return JSONResponse({'books': raw_books}, status_code = 200)
