from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import index, users, home


app = FastAPI()
# serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# add routers
app.include_router(index.router)
app.include_router(home.router)
app.include_router(users.router)

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