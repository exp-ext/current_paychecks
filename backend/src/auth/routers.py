from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_async_session
from . import crud, schemas
from .middleware import (create_access_token, get_current_user,
                         get_current_user_if_staff)

router = APIRouter()


@router.post(
    "/register/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user: schemas.UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Регистрация нового пользователя.

    Args:
    - `user`: Схема данных пользователя для создания.
    - `session`: Сессия базы данных.

    Returns:
    - Созданный пользователь.

    Raises:
    - `HTTPException` с кодом состояния 400 и деталями
    "Username already registered",
    если имя пользователя уже зарегистрировано.
    """
    db_user = await crud.get_user_by_username(session, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )
    return await crud.create_user(session=session, user=user)


@router.post("/login/")
async def login(
    user: schemas.UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Аутентификация пользователя и генерация токена доступа.

    Args:
    - `user`: Схема данных пользователя для аутентификации.
    - `session`: Сессия базы данных.

    Returns:
    - Токен доступа и тип токена.

    Raises:
    - `HTTPException` с кодом состояния 404 и деталями "User not found",
    если пользователь не найден.
    - `HTTPException` с кодом состояния 401 и деталями "Invalid password",
    если введен неправильный пароль.
    """
    db_user = await crud.get_user_by_username(session, username=user.username)

    await db_user.login(session)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not db_user.check_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    user = {"username": user.username, "password": user.password}

    access_token = create_access_token(
        user,
        timedelta(minutes=settings.access_token_expire)
    )
    return schemas.Token(
        access_token=access_token,
        token_type="Bearer"
    )


@router.get(
    "/users/",
    response_model=list[schemas.Users],
    dependencies=[Depends(get_current_user_if_staff)]
)
async def read_users(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возвращает список пользователей.

    Args:
    - `skip`: Количество записей, которое следует пропустить (по умолчанию 0).
    - `limit`: Максимальное количество записей, которое следует вернуть
    (по умолчанию 20).
    - `session`: Сессия базы данных.

    Returns:
    - Список пользователей.
    """
    return await crud.get_users(session, skip=skip, limit=limit)


@router.get("/users/me/", response_model=schemas.User)
async def read_user(
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Возвращает данные о своем профиле.

    Args:
    - `session`: Сессия базы данных.
    - `current_user`: Текущий пользователь.

    Returns:
    - Данные пользователя с указанным идентификатором.

    Raises:
    - `HTTPException` с кодом состояния 401 и деталями "Not authenticated",
    если пользователь не аутентифицирован.
    - `HTTPException` с кодом состояния 404 и деталями "User not found",
    если пользователь не найден.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    db_user = await crud.get_user_by_username(
        session, username=current_user.get('username')
    )
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch(
    "/users/get-staff-status/",
    status_code=status.HTTP_200_OK
)
async def get_staff(
    code: dict,
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Назначает юзеру статут сотрудника.

    Args:
    - `code`: Словарь с кодом авторизации.
    - `session`: Сессия базы данных.
    - `current_user`: Текущий пользователь.

    Returns:
    - Новый статут пользователя.

    Raises:
    - `HTTPException` с кодом состояния 401 и деталями "Not authenticated",
    если пользователь не аутентифицирован.
    """
    if code.get("code") != "надо":
        raise HTTPException(
            status_code=400, detail="Incorrect secret code"
        )
    db_user = await crud.set_status_staff(session, user=current_user)
    return {"Status Staff": db_user.is_staff}
