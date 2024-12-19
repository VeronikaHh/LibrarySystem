import uuid
from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db_config import get_database_session
from .models import Employee

router = APIRouter(prefix="/employees",tags=["Employee"])


@router.get("", status_code=200)
async def get_employees(session: Annotated[Session, Depends(get_database_session)]):
    employees = session.exec(select(Employee)).all()
    return employees

@router.get("/{employee_id}", status_code=200)
async def get_employee_by_id(employee_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    employee = session.get(Employee, employee_id)
    if employee is None:
        raise HTTPException()
    return employee

@router.post("", status_code=201)
async def create_employee(employee: Employee, session: Annotated[Session, Depends(get_database_session)]):
    db_employee = Employee(**employee.model_dump())
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee

@router.put("/{employee_id}", status_code=201)
async def update_employee(employee_id: uuid.UUID, employee: Employee, session: Annotated[Session, Depends(get_database_session)]):
    db_employee = session.get(Employee, employee_id)
    if db_employee is None:
        raise HTTPException()
    db_employee.sqlmodel_update(employee.model_dump())
    session.commit()
    session.refresh(db_employee)
    return db_employee

@router.delete("/{employee_id}", status_code=200)
async def delete_employee(employee_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException()
    session.delete(employee)
    session.commit()
    return {"ok": True}