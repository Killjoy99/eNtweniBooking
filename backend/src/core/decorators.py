from os import path

from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from src.core.config import settings


templates = Jinja2Templates(directory=path.join(settings.STATIC_DIR, "templates"))


def check_accept_header(request: Request) -> bool:
    """Returns true if the request is made on the browser html and false if made by application/JSONResponse

    Args:
        request (Request): default request

    Returns:
        bool: return type of the function
    """
    accept_header = request.headers.get("Accept")
    if accept_header and "text/html" in accept_header:
        return True
    return False


def render_template(request: Request, template_name: str, context: dict = None):
    if context is None:
        context = {}
    return templates.TemplateResponse(request=request, name=template_name, context=context)


def return_json(data: any):
    return JSONResponse(content=data)


async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not found"}]}
    )
