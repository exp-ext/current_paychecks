from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_db_and_tables
from .routers import routers

description = """
REST-сервис просмотра текущей зарплаты и даты следующего
повышения. 🚀
"""

app = FastAPI(
    title="API paychecks service",
    description=description,
    version="1.0.0",
    terms_of_service="http://localhost:8000/",
    contact={
        "name": "Borokin Andrey",
        "url": "https://github.com/exp-ext",
        "email": "ext77@yandex.ru",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "DELETE",
        "PATCH",
    ],
    allow_headers=["*"],
)

create_db_and_tables()

app.include_router(routers)
