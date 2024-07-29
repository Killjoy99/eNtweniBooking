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

from src.database.core import get_db
from src.core.config import STATIC_DIR
from src.core.decorators import check_accept_header, render_template, return_json

from .schemas import UserLoginResponseSchema, UserCreateSchema, UserLoginSchema, UserReadSchema, UserUpdateSchema
from .models import User

from .services import get_user_by_login_identifier


auth_router = APIRouter()
user_router = APIRouter()


# auth router related
@auth_router.get("/me", name="me")#, response_model=UserRead)
# async def get_me(*, db_session: DbSession, current_user: CurrentUser):
    # return current_user
async def get_me(request: Request, db_session: async_sessionmaker[AsyncSession]=Depends(get_db), is_template: Optional[bool] = Depends(check_accept_header)):
    if is_template:
        return render_template(request=request, template_name="me.html")
    else:
        return return_json(data={"message": "Return the logged in user"})


@auth_router.get("/signup", name="signup")
async def signup(request: Request, is_template: Optional[bool]=Depends(check_accept_header)):
    if is_template:
        data = {}
        return render_template(request=request, template_name="signup.html", context={"data": data})
    else:
        data = {}
        return return_json(data=data)

@auth_router.post("/signup", response_model=UserLoginResponseSchema)
async def signup(request: Request, user: UserCreateSchema, db_session: async_sessionmaker[AsyncSession]=Depends(get_db), is_template: Optional[bool] = Depends(check_accept_header)):
    # first check if user already exists in DB
    # statement = await db.execute(select(User).where(User.username==user.username or User.email==user.email))
    # try:
    #     user = statement.scalars().one()
    #     return user
    # #     # if not user:
    # #     #     register_user(user)
    # except Exception as e:
    #     return {"error": f"{e}"}
    
    
    
    
    hashed_pw = services.hash_password(user.password)
    user_to_db = User(username=user.username, email=user.email, password=hashed_pw)
    db.add(user_to_db)
    await db.commit()
    await db.refresh(user_to_db)
    return user_to_db
    # return services.create_access_token(user_to_db.email)


@auth_router.get("/login")
async def login(request: Request, is_template: Optional[bool]=Depends(check_accept_header)):
    if is_template:
        data = {}
        return render_template(request=request, template_name="login.html", context={"data": data})
    else:
        data = {}
        return return_json(data=data)


# login router
@auth_router.post("/login", response_model=UserLoginResponseSchema)
async def login(request: Request, user: UserLoginSchema, is_template: Optional[bool]=Depends(check_accept_header), db_session: async_sessionmaker[AsyncSession] = Depends(get_db)):
    # return await get_user_by_login_identifier(db_session=db, login_identifier=user.email)
    return user

# logout router
@auth_router.post("/logout", name="logout")
async def logout(request: Request, db_session: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Logged out"}


# User router related
@user_router.get("", name="read_users")
async def read_users():
    """adapt to Get all organisation users"""
    return {"message": "Organisation users here and paginated"}

@user_router.get("/{user_id}", name="read_user")
async def get_user(user_id: int, db_session: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Returning User with ID: {user_id}"}

@user_router.post("", name="create_user")
async def create_user(user: UserCreateSchema, db_session: async_sessionmaker[AsyncSession]=Depends(get_db)):
    # user_to_db = User(**user.dict())
    # db.add(user_to_db)
    # await db.commit()
    # await db.refresh(user_to_db)
    # return user_to_db
    return {"detail": f"Created User: {user}"}

@user_router.put("/{user_id}", name="update_user")
async def update_user(user_id: int, db_session: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Updated user {user_id}"}

@user_router.delete("/{user_id}", name="delete_user")
async def delete_user(user_id: int, db_session: async_sessionmaker[AsyncSession]=Depends(get_db)):
    return {"detail": f"Deleted user {user_id}"}

