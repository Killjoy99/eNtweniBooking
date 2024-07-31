from os import path

from functools import wraps
from fastapi import Depends, Request, status, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, Callable, Dict, Any

from src.core.config import settings


templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)


def render_template(template_name: str, context: Optional[Dict[str, Any]] = None, error_message: Optional[str] = None):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Execute the view function to get context data
            response_data = await func(request, *args, **kwargs)

            # Ensure response_data is a dictionary
            if not isinstance(response_data, dict):
                raise HTTPException(status_code=500, detail="View function did not return a dictionary.")

            ctx = context or {}
            ctx.update(response_data)

            # Include error message if provided
            if error_message:
                ctx["error_message"] = error_message

            # Render the template asynchronously
            try:
                content = templates.TemplateResponse(template_name, {"request": request, **ctx}).body.decode()
                return HTMLResponse(content=content, status_code=200)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error rendering template: {e}")

        return wrapper

    return decorator




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


def return_json(data: Any):
    return JSONResponse(content=data)


async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not found"}]}
    )
