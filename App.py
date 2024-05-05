import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routes import register_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run at startup
    print("Starting application..")
    await asyncio.create_task(register_routes(app))
    yield
    print("Shutting down..")


biblioteca = FastAPI(lifespan = lifespan, root_path = '/api')

origins = [
    "http://heyo-server"
    "http://localhost:8001"
    "https://localhost:8001"
    "http://192.168.178.101:8001"
]

biblioteca.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)


@biblioteca.get("/")
async def root():
    return {'message': 'Hello World'}
