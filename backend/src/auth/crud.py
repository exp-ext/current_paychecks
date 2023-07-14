from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_user(
    session: AsyncSession,
    user_id: int
):
    """
    Получает пользователя по идентификатору.

    Args:
    - `session`: Сеанс базы данных.
    - `user_id`: Идентификатор пользователя.

    Returns:
    - Объект модели User.
    """
    query = select(models.User).where(models.User.id == user_id)
    result = await session.execute(query)
    return result.scalars().first()


async def get_user_by_username(
    session: AsyncSession,
    username: str
):
    """
    Получает пользователя по имени пользователя.

    Args:
    - `session`: Сеанс базы данных.
    - `username`: Имя пользователя.

    Returns:
    - Объект модели User.
    """
    query = select(models.User).where(models.User.username == username)
    result = await session.execute(query)
    return result.scalars().first()


async def get_users(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 20
):
    """
    Получает список пользователей с пагинацией.

    Args:
    - `session`: Сеанс базы данных.
    - `skip`: Количество пропускаемых пользователей.
    - `limit`: Максимальное количество возвращаемых пользователей.

    Returns:
    - Список объектов модели User.
    """
    query = select(models.User).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


async def create_user(
    session: AsyncSession,
    user: schemas.UserCreate
):
    """
    Создает нового пользователя.

    Args:
    - `session`: Сеанс базы данных.
    - `user`: Схема создания пользователя.

    Returns:
    - Созданный объект модели User.
    """
    db_user = models.User(username=user.username)
    db_user.set_password(user.password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def set_status_staff(
    session: AsyncSession,
    user: schemas.User
):
    """
    Устанавливает статус "сотрудник" для пользователя.

    Args:
    - `db`: Сеанс базы данных.
    - `user`: Схема пользователя.

    Returns:
    - Обновленный объект модели User.
    """
    db_user = await get_user_by_username(
        session, username=user.get("username")
    )
    db_user.is_staff = True
    await session.commit()
    await session.refresh(db_user)
    return db_user
