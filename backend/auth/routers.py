from os import path

from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from config import STATIC_DIR


# Templates
templates = Jinja2Templates(directory=path.join(STATIC_DIR, "templates"))

auth_router = APIRouter()
user_router = APIRouter()


# User router related
@user_router.get("")
async def get_users():
    """adapt to Get all organisation users"""
    return {"message": "Organisation users here and paginated"}



# auth router related
@auth_router.get("/me", name="me")#, response_model=UserRead)
# async def get_me(*, db_session: DbSession, current_user: CurrentUser):
    # return current_user
async def get_me():
    return {"message": "Return the logged in user"}

# login auth_router
@auth_router.get("/login", name="login")
async def login(request: Request):
    return {"message": "login router"}