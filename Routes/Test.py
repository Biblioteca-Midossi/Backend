from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Utils.Database.DbHelper import Database

router = APIRouter(
    prefix = '/api',
    tags = ['test'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)


@router.get('/test')
async def test_route():
    return JSONResponse({'message': 'Test route works! Now try the others! 💀'}, status_code = 200)


@router.get('/get-test')
def db_get_test():
    try:
        with Database() as db:
            cursor = db.get_cursor()
            cursor.execute("select * from test")
            test_result = [{
                'test': result[0],
            } for result in cursor.fetchall()]
        return JSONResponse({'result': test_result}, status_code = 200)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code = 400)