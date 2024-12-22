import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from db_config import get_database_session
from .exceptions import EmployeeNotFoundError, InvalidEmployeeDataError
from .models import Employee, EmployeeCreateUpdate

router = APIRouter(prefix="/employees", tags=["Employee"])


@router.get("", status_code=200)
async def get_employees(session: Annotated[Session, Depends(get_database_session)]):
    db_employees = session.exec(select(Employee)).all()
    return db_employees


@router.get("/{employee_id}", status_code=200)
async def get_employee_by_id(employee_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    db_employee = session.get(Employee, employee_id)
    if db_employee is None:
        raise EmployeeNotFoundError(employee_id=employee_id)
    return db_employee


@router.post("", status_code=201)
async def create_employee(employee: EmployeeCreateUpdate, session: Annotated[Session, Depends(get_database_session)]):
    db_employee = Employee(**employee.model_dump())
    try:
        session.add(db_employee)
        session.commit()
        session.refresh(db_employee)
    except IntegrityError as err:
        raise InvalidEmployeeDataError(employee_id=employee.employee_id, error=str(err))
    return db_employee


@router.put("/{employee_id}", status_code=201)
async def update_employee(employee_id: uuid.UUID, employee: EmployeeCreateUpdate,
                          session: Annotated[Session, Depends(get_database_session)]):
    db_employee = session.get(Employee, employee_id)
    if db_employee is None:
        raise EmployeeNotFoundError(employee_id=employee_id)
    try:
        db_employee.sqlmodel_update(employee.model_dump())
        session.commit()
        session.refresh(db_employee)
    except IntegrityError as err:
        raise InvalidEmployeeDataError(employee_id=employee.employee_id, error=str(err))
    return db_employee


@router.delete("/{employee_id}", status_code=200)
async def delete_employee(employee_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    db_employee = session.get(Employee, employee_id)
    if not db_employee:
        raise EmployeeNotFoundError(employee_id=employee_id)
    session.delete(db_employee)
    session.commit()
    return {"ok": True}
