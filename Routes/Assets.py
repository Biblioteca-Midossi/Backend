import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(
    prefix = '/assets',
    tags = ['assets'],
    responses = {
        404: {
            "description": "Not found"
        }
    }
)


@router.get("/thumbnails/{isbn}.png")
async def get_thumbnail(isbn: str):
    try:
        thumbnail_path = f"./assets/thumbnails/{isbn}.png"
        if os.path.exists(thumbnail_path):
            return FileResponse(thumbnail_path)
        else:
            raise HTTPException(status_code = 404, detail = "Thumbnail not found")
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))


#
# @router.get("/logos/midossi.png")
# async def get_logo_midossi():
#     try:
#         path = "./assets/logos"
#         if os.path.exists(path):
#             return FileResponse("./assets/logos/midossi.png")
#         else:
#             raise HTTPException(status_code = 404, detail = "Logo not found")
#     except Exception as e:
#         raise HTTPException(status_code = 500, detail = str(e))
