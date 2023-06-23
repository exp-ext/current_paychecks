from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Базовая схема данных пользователя.

    Attributes:
    - `username`: Имя пользователя.

    """
    username: str


class UserCreate(UserBase):
    """
    Схема данных для создания пользователя.

    Attributes:
    - `username`: Имя пользователя.
    - `password`: Пароль пользователя.

    """
    password: str


class User(UserBase):
    """
    Схема данных пользователя.

    Attributes:
    - `username`: Имя пользователя.
    - `id`: Уникальный идентификатор пользователя.
    - `is_active`: Флаг активности пользователя.

    Config:
    - `orm_mode`: Режим работы с ORM.

    """
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Users(User):
    """
    Схема данных для списка пользователей.

    Attributes:
    - `username`: Имя пользователя.
    - `id`: Уникальный идентификатор пользователя.
    - `is_active`: Флаг активности пользователя.
    - `last_login`: Дата последней авторизации пользователя.
    - `is_staff`: Флаг принадлежности пользователя к персоналу.

    """
    last_login: Optional[datetime]
    is_staff: bool


class UserLogin(BaseModel):
    """
    Схема данных для входа пользователя.

    Attributes:
    - `username`: Имя пользователя.
    - `password`: Пароль пользователя.

    """
    username: str
    password: str


class Token(BaseModel):
    """
    Схема данных токена доступа.

    Attributes:
    - `access_token`: Токен доступа.
    - `token_type`: Тип токена.

    """
    access_token: str
    token_type: str
