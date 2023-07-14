from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, event
from sqlalchemy.orm import relationship

from ..database import Base


class Salary(Base):
    """
    Модель данных о зарплате сотрудника.

    Attributes:
    - `id`: Уникальный идентификатор.
    - `employee_id`: Идентификатор сотрудника, связь с моделью `User`.
    - `current_rate`: Текущая ставка зарплаты.
    - `rate_increase_period`: Период повышения ставки зарплаты (в днях).
    - `last_promotion_date`: Дата последнего повышения зарплаты.

    Relationships:
    - `employee`: Связь с моделью `User`, обратное отношение "один к одному".
    """

    __tablename__ = "salaries"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    current_rate = Column(Float)
    rate_increase_period = Column(Integer)
    last_promotion_date = Column(TIMESTAMP)

    employee = relationship("User", back_populates="salaries")

    @classmethod
    def __declare_last__(cls):
        """
        Обработчик события для автоматического обновления даты последнего
        повышения при изменении ставки зарплаты.

        Notes:
        - Метод срабатывает при изменении значения атрибута
        `current_rate` модели.

        Args:
        - `target`: Ссылка на экземпляр модели.
        - `value`: Новое значение атрибута.
        - `oldvalue`: Старое значение атрибута.
        - `initiator`: Инициатор события.

        Returns:
        - None.
        """

        @event.listens_for(cls.current_rate, "set")
        def receive_set(target, *args, **kwargs):
            target.last_promotion_date = datetime.now()
