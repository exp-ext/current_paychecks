from sqlalchemy.orm import Session

from ..auth.models import User
from . import models, schemas


def get_employee_by_id(
    db: Session,
    id: int
):
    return db.query(User).filter(User.id == id).first()


def create_an_employee_salary(
    db: Session,
    salary: schemas.SalaryCreate
):
    db_salary = models.Salary(**salary.dict())
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary


def get_salaries_by_username(
    db: Session,
    username: str
):
    user = db.query(User).join(User.salaries).filter(
        User.username == username
    ).first()
    if user:
        return user.salaries.all()
    return []
