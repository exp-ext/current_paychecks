from datetime import datetime, timedelta

import jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import crud
from ..config import settings
from ..database import get_async_session

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta):
    """
    Создает токен доступа.

    Args:
    - `data`: Данные, которые будут включены в токен.
    - `expires_delta`: Временной промежуток до истечения срока действия токена.

    Returns:
    - Сгенерированный токен доступа.
    """
    payload = data.copy()
    expire = datetime.utcnow() + expires_delta
    payload.update({"exp": expire})
    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    """
    Расшифровывает токен.

    Args:
    - `token`: Токен, который нужно расшифровать.

    Returns:
    - Расшифрованный токен.

    Exception:
    - `HTTPException` с кодом состояния 401 и деталями "Token expired" при
    истечении срока действия токена.
    - `HTTPException` с кодом состояния 401 и деталями "Invalid token" при
    недействительном токене.
    """
    try:
        decoded_token = jwt.decode(
            token, settings.secret_key, algorithms=[ALGORITHM]
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(
    token: str = Security(oauth2_scheme),
) -> dict:
    """
    Получает текущего пользователя.

    Args:
    - `token`: Токен доступа пользователя.

    Returns:
    - Данные текущего пользователя из расшифрованного токена.

    Exception:
    - `HTTPException` с кодом состояния 401 и деталями "Invalid token" при
    недействительном токене или отсутствующем имени пользователя.
    """
    payload = decode_token(token)
    username = payload.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


async def get_current_user_if_staff(
    token: str = Security(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Проверяет токен текущего юзера и статус staff.

    Args:
    - `token`: Токен доступа сотрудника.
    - `session`: Сессия базы данных.

    Returns:
    - Данные текущего сотрудника из расшифрованного токена.

    Exception:
    - `HTTPException` с кодом состояния 401 и деталями "Invalid token" при
    недействительном токене или отсутствующем имени пользователя.
    - `HTTPException` с кодом состояния 403 и деталями "User is not a staff
    member" при отсутствии у пользователя статуса сотрудника.
    """
    payload = decode_token(token)
    username = payload.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_user = await crud.get_user_by_username(session, username=username)
    if not db_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a staff member"
        )
    return payload
