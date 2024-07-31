import logging

from os import path
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_offline import FastAPIOffline
from fastapi.responses import PlainTextResponse
from fastapi.exception_handlers import http_exception_handler

from fastapi_limiter import FastAPILimiter

from sqladmin import Admin

from src.core.config import settings
from src.database.core import async_engine
from src.core.decorators import render_template
from src.admin.admin import UserAdmin, OrganisationAdmin, ProductAdmin, BookingAdmin
from src.core.decorators import templates

from .api import api_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        # Add more handlers if needed, e.g., FileHandler
    ]
)
logger = logging.getLogger(__name__)


app = FastAPI(openapi_url="")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust according to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
# app.add_middleware(
#     FastAPILimiter,
#     rate_limit="5/minute"        # Adjust according to your needs
# )

frontend = FastAPI(openapi_url="")
api = FastAPIOffline(
    title="eNtweniBooking",
    description="Welcome to eNtweniBooking's API documentation!",
    root_path="/api/v1",
    version="0.1.2",
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)

admin = Admin(api, async_engine)
admin.add_view(UserAdmin)
admin.add_view(OrganisationAdmin)
admin.add_view(ProductAdmin)
admin.add_view(BookingAdmin)


@frontend.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request path: {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status code: {response.status_code}")
    return response

@frontend.middleware("http")
async def default_page(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        # Render the 404 page using the custom template
        template_response = templates.TemplateResponse("404.html", {"request": request, "data": {}, "error_message": "Not Found"})
        return HTMLResponse(content=template_response.body.decode(), status_code=404)
    return response

# @frontend.exception_handler(HTTPException)
# async def custom_http_exception_handler(request: Request, exc: HTTPException):
#     return HTMLResponse(
#         content=templates.TemplateResponse("500.html", {"request": request, "error_message": exc.detail}).body.decode(),
#         status_code=exc.status_code
#     )

# @frontend.exception_handler(Exception)
# async def general_exception_handler(request: Request, exc: Exception):
#     return HTMLResponse(
#         content=templates.TemplateResponse("500.html", {"request": request, "error_message": "Internal Server Error"}).body.decode(),
#         status_code=500
#     )
    
    
@frontend.get("/", name="index")
@render_template(template_name="index.html")
async def index(request: Request):
    return {"data": {}, "error_message": None}


if settings.STATIC_DIR and path.isdir(settings.STATIC_DIR):
    # Consider changing the route for static files to avoid conflicts
    frontend.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

api.include_router(api_router)

app.mount("/api/v1", app=api)
app.mount("/", app=frontend)
