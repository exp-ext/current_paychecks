from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Возвращает экземпляр сессии базы данных.

    Yields:
    - Сессия базы данных.

    Closes:
    - Закрывает сессию базы данных после использования.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Создает таблицы в базе данных.

    Notes:
    - Для создания таблиц необходимо импортировать модели данных
    (модели, унаследованные от Base).
    """
    Base.metadata.create_all(bind=engine)
