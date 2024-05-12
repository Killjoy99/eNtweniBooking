from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models.user import User

templates = Jinja2Templates(directory="templates")
app = FastAPI()

origins = [
    "http://localhost:8000",
    "localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", response_class=HTMLResponse, tags=["home"])
async def index(request: Request):
    data = {"message": "Welcome to eNtweni Bookings"}
    
    if "application/json" in request.headers.get("Accept", ""):
        return JSONResponse(data)

    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.post("/register", response_class=HTMLResponse, tags=["home"])
async def login(request: Request, user: User):
    # try to login with supplied credentials
    registered = do_register(remember_me=user.remember_me, username=user.username, password=user.password)
    registered_status = {"status": logged_in}
        
    if "application/json" in request.headers.get("Accept", ""):
        return JSONResponse(registered_status)

    return templates.TemplateResponse("home.html", {"request": request, "user": user, "logged_in_status": logged_in_status})


def do_login(remember_me: bool = False, username: str = None, password: str = None):
    if username != "admin" or password != "admin123":
        return False
    else:
        return True
    

@app.post("/login", response_class=HTMLResponse, tags=["home"])
async def login(request: Request, user: User):
    # try to login with supplied credentials
    logged_in = do_login(remember_me=user.remember_me, username=user.username, password=user.password)
    logged_in_status = {"status": logged_in}
        
    if "application/json" in request.headers.get("Accept", ""):
        return JSONResponse(logged_in_status)

    return templates.TemplateResponse("home.html", {"request": request, "user": user, "logged_in_status": logged_in_status})




# A websocket for android client connection
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.send_json({"message": data})