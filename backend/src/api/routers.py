from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import crud as user_crud
from ..auth.middleware import get_current_user, get_current_user_if_staff
from ..database import engine, get_db
from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/api/salary",
    tags=["salary"]
)


@router.post(
    "/set-rate/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user_if_staff)]
)
def create_salary(
    salary: schemas.SalaryCreate,
    db: Session = Depends(get_db),
):
    """
    Устанавливает ставку зарплаты для сотрудника.

    Args:
    - `salary`: Схема создания зарплаты сотрудника.
    - `db`: Сеанс базы данных.

    Returns:
    - Созданный объект модели зарплаты.
    """
    db_user = user_crud.get_user(db, id=salary.employee_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail="No such user"
        )
    return crud.create_an_employee_salary(db, salary=salary)


@router.get(
    "/next-pay-raise/",
    status_code=status.HTTP_200_OK
)
def get_next_pay_raise(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Получает ставку и дату следующего повышения зарплаты.

    Args:
    - `db`: Сеанс базы данных.
    - `current_user`: Текущий аутентифицированный пользователь.

    Returns:
    - Словарь с текущей ставкой и датой следующего повышения зарплаты.
    """
    salaries = crud.get_salaries_by_username(
        db, username=current_user.get('username')
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
