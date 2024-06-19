from os import path
from typing import Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form

from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncAttrs, AsyncSession
from database.core import get_db

from .schemas import UserCreate, UserLogin

from core.config import STATIC_DIR

from core.decorators import check_accept_header, render_template, return_json


auth_router = APIRouter()
user_router = APIRouter()


# auth router related
@auth_router.get("/me", name="me")#, response_model=UserRead)
# async def get_me(*, db_session: DbSession, current_user: CurrentUser):
    # return current_user
async def get_me(request: Request, db: async_sessionmaker[AsyncSession]=Depends(get_db), is_template: Optional[bool] = Depends(check_accept_header)):
    if is_template:
        return render_template(request=request, template_name="me.html")
    else:
        return return_json(data={"message": "Return the logged in user"})

@auth_router.get("/login")
async def login(request: Request, is_template: Optional[bool]=Depends(check_accept_header)):
    if is_template:
        data = {}
        return render_template(request=request, template_name="login.html", context={"item": data})
    else:
        data = {}
        return return_json(data=data)


# login router
@auth_router.post("/login")
async def login(request: Request, user: UserLogin, db: async_sessionmaker[AsyncSession]=Depends(get_db), is_template: Optional[bool]=Depends(check_accept_header)):
    # statement = await db.execute(select(User).where(User.username==username and User.password==password))
    # try:
    #     user = statement.scalars().one()
    #     if user:
    #         login_user(user)
    # except:
    #     return {"error": "Incorrect Username or Password"}
    
    if user.username != "admin" or user.password != "admin123":
        data = {"error": "Incorrect username or password", "status": False}
        if is_template:
            return render_template(request=request, template_name="login.html", context={"item": data})
        else:
            return return_json(data=data)
    else:
        data = {"detail": f"Logged In Successful", "status": True}
        if is_template:
            return render_template(request=request, template_name="login.html", context={"item": data})
        else:
            return return_json(data=data)

# logout router
@auth_router.post("/logout", name="logout")
async def logout(request: Request, db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Logged out"}


# User router related
@user_router.get("", name="read_users")
async def read_users():
    """adapt to Get all organisation users"""
    return {"message": "Organisation users here and paginated"}

@user_router.get("/{user_id}", name="read_user")
async def get_user(user_id: int, db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Returning User with ID: {user_id}"}

@user_router.post("", name="create_user")
async def create_user(user: UserCreate, db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Created User: {user}"}

@user_router.put("/{user_id}", name="update_user")
async def update_user(user_id: int, db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Updated user {user_id}"}

@user_router.delete("/{user_id}", name="delete_user")
async def delete_user(user_id: int, db: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Deleted user {user_id}"}

