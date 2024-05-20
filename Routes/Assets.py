import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(
    prefix = '/assets',
    tags = ['assets'],
    responses = {
        404: {
            "description": "Not found"
        },
        200: {
            "content": {"image/png": {}}
        }
    },
)


@router.get("/thumbnails/{book_id}.png", response_class = FileResponse)
async def get_thumbnail(book_id: int):
    """
    Get the thumbnail image for a book by its ISBN.
    
    **Path**: `/assets/thumbnails/{isbn}.png`
    
    **Method**: `GET`
    
    **Description**:
    Retrieves the thumbnail image for a book identified by its ID.
    
    **Arguments**:
    - `book_id` int: The ID of the book to retrieve the thumbnail for.
    
    **Returns**:
    - FileResponse: The PNG thumbnail image with status code 200 if found.
    - HTTPException: If the thumbnail is not found (404) or if there is an error (500).
    
    **Raises**:
    - HTTPException: If the thumbnail is not found.
    - HTTPException: If there is an error retrieving the thumbnail.
    """
    try:
        thumbnail_path = f"./assets/thumbnails/{book_id}.png"
        if os.path.exists(thumbnail_path):
            return FileResponse(thumbnail_path)
        else:
            raise HTTPException(status_code = 404, detail = "Thumbnail not found")
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))


#
# @router.get("/logos/midossi.png")
# async def get_logo_midossi():
    """
    Get the Midossi logo image.
    
    **Path**: `/assets/logos/midossi.png`
    
    **Method**: `GET`
    
    **Description**:
    Retrieves the Midossi logo image.
    
    **Returns**:
    - FileResponse: The PNG logo image with status code 200 if found.
    - HTTPException: If the logo is not found (404) or if there is an error (500).
    
    **Raises**:
    - HTTPException: If the logo is not found.
    - HTTPException: If there is an error retrieving the logo.
    """
#     try:
#         path = "./assets/logos"
#         if os.path.exists(path):
#             return FileResponse("./assets/logos/midossi.png")
#         else:
#             raise HTTPException(status_code = 404, detail = "Logo not found")
#     except Exception as e:
#         raise HTTPException(status_code = 500, detail = str(e))
