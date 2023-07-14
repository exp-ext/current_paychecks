from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import crud as user_crud
from ..auth.middleware import get_current_user, get_current_user_if_staff
from ..database import get_async_session
from . import crud, schemas

router = APIRouter()


@router.post(
    "/set-rate/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user_if_staff)]
)
async def create_salary(
    salary: schemas.SalaryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Устанавливает ставку зарплаты для сотрудника.

    Args:
    - `salary`: Схема создания зарплаты сотрудника.
    - `session`: Сеанс базы данных.

    Returns:
    - Созданный объект модели зарплаты.
    """
    db_user = await user_crud.get_user(session, user_id=salary.employee_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail="No such user"
        )
    return await crud.create_an_employee_salary(session, salary=salary)


@router.get(
    "/next-pay-raise/",
    status_code=status.HTTP_200_OK
)
async def get_next_pay_raise(
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Получает ставку и дату следующего повышения зарплаты.

    Args:
    - `session`: Сеанс базы данных.
    - `current_user`: Текущий аутентифицированный пользователь.

    Returns:
    - Словарь с текущей ставкой и датой следующего повышения зарплаты.
    """
    salaries = await crud.get_salaries_by_username(
        session, username=current_user.get('username')
    )
    if len(salaries) == 0:
        raise HTTPException(
            status_code=404,
            detail="You are not yet registered as an employee."
        )

    return {
        "current rate": salaries[-1].current_rate,
        "next raise date": (
            salaries[-1].last_promotion_date + timedelta(
                days=salaries[-1].rate_increase_period)
        ).strftime("%d.%m.%Y")
    }
