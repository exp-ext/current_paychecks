from datetime import datetime, timezone

from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import Session, relationship

from ..database import Base

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """
    Модель данных о пользователе.

    Attributes:
    - `id`: Уникальный идентификатор.
    - `username`: Имя пользователя.
    - `email`: Электронная почта пользователя.
    - `hashed_password`: Хэшированный пароль пользователя.
    - `last_login`: Дата последней авторизации пользователя.
    - `is_active`: Флаг активности пользователя.
    - `is_staff`: Флаг принадлежности пользователя к персоналу.

    Relationships:
    - `salaries`: Связь с моделью `Salary`, обратное отношение
    "один ко многим".

    Methods:
    - `set_password()`: Задает хэш пароля пользователя.
    - `check_password()`: Проверяет соответствие пароля хэшу.
    - `login()`: Выполняет операцию авторизации пользователя.

    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)

    last_login = Column(DateTime)

    is_active = Column(Boolean(), default=True)
    is_staff = Column(Boolean(), default=False)

    salaries = relationship(
        "Salary", back_populates="employee", lazy="dynamic"
    )

    def set_password(self, password: str):
        """
        Задает хэш пароля пользователя.

        Args:
        - `password`: Пароль пользователя.

        Returns:
        - None.
        """
        self.hashed_password = password_context.hash(password)

    def check_password(self, password: str) -> bool:
        """
        Проверяет соответствие пароля хэшу.

        Args:
        - `password`: Пароль для проверки.

        Returns:
        - True, если пароль соответствует хэшу, иначе False.
        """
        return password_context.verify(password, self.hashed_password)

    def login(self, db: Session):
        """
        Выполняет операцию авторизации пользователя.

        Args:
        - `db`: Сессия базы данных.

        Returns:
        - None.
        """
        self.last_login = datetime.now(timezone.utc)
        db.add(self)
        db.commit()
