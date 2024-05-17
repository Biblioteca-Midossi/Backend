import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routes import register_routes
from Utils.Logger import setup_logger


setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run at startup
    print("Starting application..")
    await asyncio.create_task(register_routes(app))
    yield
    print("Shutting down..")


biblioteca = FastAPI(
    lifespan = lifespan, 
    root_path = '/api', 
    swagger_ui_parameters={
        "syntaxHighlight.theme": "obsidian"
        }
    )

origins = [
    "http://127.0.0.1",
    "http://localhost:8001",
    "https://localhost:8001",
]

biblioteca.add_middleware(
    CORSMiddleware,
    # allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
    allow_origin_regex = "(https?:\/\/)?(192)\.(168)(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])){2}(?::8001)?|localhost(?::8001)?|127.0.0.1(?::8001)?"
)


@biblioteca.get("/")
async def root():
    return {'message': 'Hello World'}
