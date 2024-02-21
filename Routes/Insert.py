from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix = '/api',
    tags = ['insert'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)


@router.post("/insert")
async def insert(request: Request):
    try:
        data = await request.json()
        print(data)
        return JSONResponse({"status": "successful"}, status_code = 200)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code = 400)
