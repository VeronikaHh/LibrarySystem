import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from db_config import get_database_session
from .exceptions import EmployeeNotFoundException, InvalidEmployeeDataException
from .models import Employee, EmployeeCreateUpdate

router = APIRouter(prefix="/employees", tags=["Employee"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_employees(session: Annotated[Session, Depends(get_database_session)]):
    db_employees = session.exec(select(Employee)).all()
    return db_employees


@router.get("/{employee_id}", status_code=status.HTTP_200_OK)
async def get_employee_by_id(employee_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    db_employee = session.get(Employee, employee_id)
    if db_employee is None:
        raise EmployeeNotFoundException(employee_id=employee_id)
    return db_employee


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreateUpdate, session: Annotated[Session, Depends(get_database_session)]):
    db_employee = Employee(**employee.model_dump())
    try:
        session.add(db_employee)
        session.commit()
        session.refresh(db_employee)
    except IntegrityError as err:
        raise InvalidEmployeeDataException(employee_id=employee.employee_id, error=str(err))
    return db_employee


@router.put("/{employee_id}", status_code=status.HTTP_200_OK)
async def update_employee(employee_id: uuid.UUID, employee: EmployeeCreateUpdate,
                          session: Annotated[Session, Depends(get_database_session)]):
    db_employee = session.get(Employee, employee_id)
    if db_employee is None:
        raise EmployeeNotFoundException(employee_id=employee_id)
    try:
        db_employee.sqlmodel_update(employee.model_dump())
        session.commit()
        session.refresh(db_employee)
    except IntegrityError as err:
        raise InvalidEmployeeDataException(employee_id=employee.employee_id, error=str(err))
    return db_employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    db_employee = session.get(Employee, employee_id)
    if not db_employee:
        raise EmployeeNotFoundException(employee_id=employee_id)
    session.delete(db_employee)
    session.commit()
    return {"ok": True}
