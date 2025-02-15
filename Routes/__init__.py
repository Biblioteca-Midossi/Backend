from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from Routes import Assets, Auth, Books, Test, Users


async def register_routes(app: FastAPI):
    @app.get('/favicon.ico', include_in_schema = False)
    async def favicon():
        return FileResponse('favicon.ico')

    app.include_router(Assets.router)
    app.include_router(Auth.router)
    app.include_router(Books.router)
    app.include_router(Test.router)
    app.include_router(Users.router)
    