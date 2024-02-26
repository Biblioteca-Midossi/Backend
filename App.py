from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routes import register_routes


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)


@app.on_event('startup')
async def startup_event():
    register_routes(app)


@app.get("/")
async def root():
    return {'message': 'Hello World'}
