from os import path
from typing import Optional, List

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.routing import compile_path

from api import api_router
# from .common.utils.cli import install_plugins, install_plugin_events
from core.config import STATIC_DIR
# from .rate_limiter import limiter

from auth.routers import auth_router, user_router

from fastapi_offline import FastAPIOffline          #NOTE:  Change to FastAPI on runtime


async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not found"}]}
    )
    

exception_handlers = {404: not_found}

# Templates
templates = Jinja2Templates(directory=path.join(STATIC_DIR, "templates"))


# create ASGI for the app
app = FastAPI(exception_handlers=exception_handlers, openapi_url="")
# app.state.limiter = limiter      # for rate limiting
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# create ASGI for the frontend
frontend = FastAPI(openapi_url="")


@frontend.middleware("http")
async def default_page(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        if STATIC_DIR:
            return templates.TemplateResponse(request=request, name="404.html")
    return response


# create the Web API Framework
api = FastAPIOffline(
    title="eNtweniBooking",
    description="Welcome to eNtweniBooking's API documentation! Here you will able to discover all of the ways you can interact with the eNtweniBooking API.",
    root_path="/api/v1",
    version="0.0.1",
    # docs_url=None,
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)

# load static files for api
api.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

api.include_router(api_router)


# mount static files for the frontend
if STATIC_DIR and path.isdir(STATIC_DIR):
    frontend.mount("/", StaticFiles(directory=STATIC_DIR), name="app")

# we mount the frontend and api
app.mount("/api/v1", app=api)
app.mount("/", app=frontend)