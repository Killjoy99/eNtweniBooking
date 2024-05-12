from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware


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

# A websocket for android client connection
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.send_json({"message": data})