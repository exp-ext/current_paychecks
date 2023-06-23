from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SalaryBase(BaseModel):
    """
    Базовая схема данных для зарплаты.

    Attributes:
    - `employee_id`: Уникальный идентификатор сотрудника.
    - `current_rate`: Текущая ставка зарплаты.
    - `rate_increase_period`: Период повышения зарплаты.

    """
    employee_id: int
    current_rate: float
    rate_increase_period: int


class SalaryCreate(SalaryBase):
    """
    Схема данных для создания записи о зарплате.

    Наследуется от базовой схемы `SalaryBase`.

    """
    pass


class SalaryUpdate(SalaryBase):
    """
    Схема данных для обновления записи о зарплате.

    Наследуется от базовой схемы `SalaryBase`.

    Attributes:
    - `employee_id`: Уникальный идентификатор сотрудника.
    - `current_rate`: Текущая ставка зарплаты.
    - `rate_increase_period`: Период повышения зарплаты.
    - `last_promotion_date`: Дата последнего повышения зарплаты (опционально).

    """
    last_promotion_date: Optional[datetime] = None


class SalaryInDB(SalaryBase):
    """
    Схема данных для записи о зарплате из базы данных.

    Наследуется от базовой схемы `SalaryBase`.

    Attributes:
    - `id`: Уникальный идентификатор записи о зарплате.
    - `employee_id`: Уникальный идентификатор сотрудника.
    - `current_rate`: Текущая ставка зарплаты.
    - `rate_increase_period`: Период повышения зарплаты.

    Config:
    - `orm_mode`: Режим работы с ORM.

    """
    id: int
    employee_id: int

    class Config:
        orm_mode = True
