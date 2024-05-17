from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from Utils.Database.DbHelper import Database

router = APIRouter(
    tags = ['test'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)


@router.get('/test')
async def test_route():
    """
    Test Route
    
    **Path**: `/test`
    
    **Method**: `GET`
    
    **Description**:
    This endpoint serves as a basic test to confirm that the API is up and running.
    
    **Returns**:
    - `JSONResponse`: A message confirming that the test route works, with a status code of 200.
    """
    return JSONResponse({'message': 'Test route works! Now try the others! 💀'}, status_code = 200)


@router.get('/get-test')
def db_get_test():
    """
    Database Get Test
    
    **Path**: `/get-test`
    
    **Method**: `GET`
    
    **Description**:
    This endpoint connects to the database, executes a query to fetch all rows from the 'test' table,
    and returns the results in JSON format.
    
    **Returns**:
    - `JSONResponse`: A JSON object containing a list of test results with a status code of 200.
    - `JSONResponse`: A JSON object containing an error message with a status code of 400 if an exception occurs.
    
    **Raises**:
    - `Exception`: If there is an error connecting to the database or executing the query.
    """
    try:
        with Database() as db:
            cursor = db.get_cursor()
            cursor.execute("select * from test")
            test_result = [{
                'test': result[0],
            } for result in cursor.fetchall()]
        return JSONResponse({'result': test_result}, status_code = 200)
    except Exception as e:
        return HTTPException(status_code = 400, detail = f'Error: {e}')