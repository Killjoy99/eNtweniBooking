from os import path
from typing import Optional, List

from fastapi import FastAPI, status, Depends
from fastapi_offline import FastAPIOffline          #NOTE:  Change to FastAPI on runtime
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.routing import compile_path

from src.core.config import settings
from src.core.decorators import render_template, check_accept_header

from .api import api_router


# create ASGI for the app
app = FastAPI(openapi_url="")

# create ASGI for the frontend
frontend = FastAPI(openapi_url="")

# create the Web API Framework
api = FastAPIOffline(
    title="eNtweniBooking",
    description="Welcome to eNtweniBooking's API documentation! Here you will able to discover all of the ways you can interact with the eNtweniBooking API.",
    root_path="/api/v1",
    version="0.1.2",
    # docs_url=None,
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)

@frontend.get("/")
async def index(request: Request):
    return render_template(request=request, template_name="index.html")

@frontend.middleware("http")
async def default_page(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        if settings.STATIC_DIR:
            return render_template(request=request, template_name="404.html")
    return response

# mount static files for the frontend
if settings.STATIC_DIR and path.isdir(settings.STATIC_DIR):
    frontend.mount("/", StaticFiles(directory=settings.STATIC_DIR), name="static")


api.include_router(api_router)

# we mount the frontend and api
app.mount("/api/v1", app=api)
app.mount("/", app=frontend)