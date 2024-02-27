from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from Utils.Database.DbHelper import Database
from math import isnan

router = APIRouter(
    prefix = '/api',
    tags = ['insert'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)


def insert_collocazione(collocazione):
    if not isnan(collocazione.get('istituto')):
        # switch con numero?
        # select biblioteca.istituti where nome_istituto = x?
        pass

    with Database() as db:
        cursor = db.get_cursor()
        cursor.execute(f'insert into biblioteca.collocazioni(id_istituto, scaffale)')


def insert_autore():
    pass


def insert_libro():
    pass


async def insert_book_into_database(data):
    autore = {
        'nome': data[0],
        'cognome': data[1],
    }
    libro = {
        'isbn': data[2],
        'titolo': data[3],
        'quantita': data[4],
        'casa_editrice': data[5],
        'descrizione': data[6],
    }
    collocazione = {
        'istituto': data[7],
        'collocazione': data[8],
    }

    insert_collocazione(collocazione)
    insert_autore()
    insert_libro()


@router.post("/insert")
async def insert(request: Request):
    try:
        data = await request.json()
        for entry in data:
            if entry is not data[6] and entry == '':
                return JSONResponse({'error': 'Bad request'}, status_code = 400)

        # add entry to database
        await insert_book_into_database(data)

        return JSONResponse({"status": "successful"}, status_code = 200)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code = 400)
