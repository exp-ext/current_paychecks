from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.crud import get_user_by_username
from . import models, schemas


async def create_an_employee_salary(
    session: AsyncSession,
    salary: schemas.SalaryCreate
):
    db_salary = models.Salary(**salary.dict())
    session.add(db_salary)
    await session.commit()
    await session.refresh(db_salary)
    return db_salary


async def get_salaries_by_username(
    session: AsyncSession,
    username: str
):
    user = await get_user_by_username(session, username)
    query = (
        select(models.Salary).where(models.Salary.employee.has(id=user.id))
    )
    result = await session.execute(query)
    return result.scalars().all()
