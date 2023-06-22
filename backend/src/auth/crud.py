from sqlalchemy.orm import Session

from . import models, schemas


def get_user(
    db: Session,
    user_id: int
):
    """
    Получает пользователя по идентификатору.

    Args:
    - `db`: Сеанс базы данных.
    - `user_id`: Идентификатор пользователя.

    Returns:
    - Объект модели User.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(
    db: Session,
    username: str
):
    """
    Получает пользователя по имени пользователя.

    Args:
    - `db`: Сеанс базы данных.
    - `username`: Имя пользователя.

    Returns:
    - Объект модели User.
    """
    return db.query(models.User).filter(
        models.User.username == username
    ).first()


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 20
):
    """
    Получает список пользователей с пагинацией.

    Args:
    - `db`: Сеанс базы данных.
    - `skip`: Количество пропускаемых пользователей.
    - `limit`: Максимальное количество возвращаемых пользователей.

    Returns:
    - Список объектов модели User.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(
    db: Session,
    user: schemas.UserCreate
):
    """
    Создает нового пользователя.

    Args:
    - `db`: Сеанс базы данных.
    - `user`: Схема создания пользователя.

    Returns:
    - Созданный объект модели User.
    """
    db_user = models.User(username=user.username)
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def set_status_staff(
    db: Session,
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
    db_user = get_user_by_username(db, username=user.get("username"))
    db_user.is_staff = True
    db.commit()
    db.refresh(db_user)
    return db_user
