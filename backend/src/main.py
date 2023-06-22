from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import routers as api
from .auth import routers as auth
from .database import create_tables
from .routers import router as docs

origins = []

app = FastAPI()

app.include_router(auth.router)
app.include_router(api.router)
app.include_router(docs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()
