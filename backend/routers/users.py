from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi import APIRouter, Request, Form, Depends, Body

from typing import Optional

from services.authentication import AuthenticationService
from models.user import User
from forms.auth import LoginForm


templates = Jinja2Templates(directory="static/templates")
router = APIRouter()


@router.get("/register", response_class=HTMLResponse, tags=["auth"])
async def register_get(request: Request):
    # this is for rendering login page
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register/", response_class=HTMLResponse, tags=["auth"])
async def register_post(request: Request, user: User):
    # try to login with supplied credentials
    registered = AuthenticationService().register(remember_me=user.remember_me, username=user.username, password=user.password)
    registered_status = {"status": logged_in}
        
    if "application/json" in request.headers.get("Accept", ""):
        return JSONResponse(registered_status)

    return templates.TemplateResponse("home.html", {"request": request, "user": user, "logged_in_status": logged_in_status})

@router.get("/login/", response_class=HTMLResponse, tags=["auth"], name="login")
async def login_get(request: Request):
    # this is for rendering login page
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login/", response_class=HTMLResponse, tags=["auth"], name="login")
async def login_post(request: Request, user: Optional[User] = Body(None), username: Optional[str] = Form(None), password: Optional[str] = Form(None), remember_me: Optional[bool] = Form(None)):
    # try to login with supplied credentials
    # print(username)
    try:
            
        if "application/json" in request.headers.get("Accept", ""):
            print(user)
            logged_in = AuthenticationService().login(remember_me=user.remember_me, username=user.username, password=user.password)
            logged_in_status = {"status": logged_in}
                
            return JSONResponse(logged_in_status)
        
        elif "text/html" in request.headers.get("Accept", ""):
            logged_in = AuthenticationService().login(remember_me=remember_me, username=username, password=password)
            logged_in_status = {"status": logged_in}
            
            if logged_in:
                return templates.TemplateResponse("home.html", {"request": request, "username": username})
            else:
                # return RedirectResponse("login")
                pass
    except Exception as e:
        print(e)
    # form = LoginForm(request)
    # nf = await form.load_data()
    # print(nf)
    
    # if form.is_valid():
    #     try:
    #         logged_in = AuthenticationService().login(remember_me=form.remember_me, username=form.username, password=form.password)
    #         logged_in_status = {"status": logged_in}
    #         user = form.__dict__
    #         print(user)
    #     except Exception as e:
    #         print(e)
    #         # form.__dict__.get()
    #         return templates.TemplateResponse("login.html", {"user": form.__dict__})
    # return templates.TemplateResponse("home.html", {"request": request})
    # return templates.TemplateResponse("home.html", {"request": request,"logged_in_status": logged_in_status})