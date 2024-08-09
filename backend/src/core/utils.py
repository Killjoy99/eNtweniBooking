from fastapi import Request
from fastapi.templating import Jinja2Templates

from core.config import settings

templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)


def check_accept_header(request: Request) -> bool:
    """Returns true if the request is made on the browser html and false if made by application/JSONResponse

    Args:
        request (Request): default request

    Returns:
        bool: return type of the function
    """
    accept_header = request.headers.get("Accept")
    return "text/html" in accept_header if accept_header else False
