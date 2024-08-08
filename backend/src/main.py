import logging
from os import path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_offline import FastAPIOffline
from pyinstrument import Profiler
from pyinstrument.renderers.html import HTMLRenderer  # noqa: F401
from sqladmin import Admin

from src.admin.admin import BookingAdmin, OrganisationAdmin, ProductAdmin, UserAdmin
from src.core.config import settings
from src.core.utils import templates
from src.database.core import async_engine

from .api import api_router


class PyInstrumentMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            profiler = Profiler()
            profiler.start()
            await self.app(scope, receive, send)
            profiler.stop()
            profiler.open_in_browser()
        else:
            await self.app(scope, receive, send)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        # Add more handlers if needed, e.g., FileHandler
    ],
)
logger = logging.getLogger(__name__)


app = FastAPI(openapi_url="")

app.add_middleware(PyInstrumentMiddleware)
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
async def default_page(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        # Render the 404 page using the custom template
        template_response = templates.TemplateResponse(
            "404.html", {"request": request, "data": {}, "error_message": "Not Found"}
        )
        return HTMLResponse(content=template_response.body.decode(), status_code=404)
    return response


@frontend.get("/", name="index")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


if settings.STATIC_DIR and path.isdir(settings.STATIC_DIR):
    # Consider changing the route for static files to avoid conflicts
    frontend.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

api.include_router(api_router)

app.mount("/api/v1", app=api)
app.mount("/", app=frontend)
