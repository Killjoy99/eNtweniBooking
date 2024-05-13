from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import APIRouter, Request


templates = Jinja2Templates(directory="static/templates")
router = APIRouter()

@router.get("/home", response_class=HTMLResponse, tags=["home"], name="home")
async def index(request: Request):
    data = {"message": "eNtweni Bookings"}
    
    if "application/json" in request.headers.get("Accept", ""):
        return JSONResponse(data)

    return templates.TemplateResponse("home.html", {"request": request, "data": data})


# A websocket for android client connection
# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_json()
#         await websocket.send_json({"message": data})