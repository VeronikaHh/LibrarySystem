import uuid
from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.db_config import get_database_session
from .exceptions import EmployeeNotFoundException, InvalidEmployeeDataException
from .models import Employee, EmployeeCreateUpdate


class EmployeeDataAccessLayer:
    def __init__(self, session: Annotated[Session, Depends(get_database_session)]):
        self.__session = session

    def get_all_employees(self) -> Sequence[Employee]:
        db_employees = self.__session.exec(select(Employee)).all()
        return db_employees

    def get_employee_by_id(self, employee_id: uuid.UUID) -> Employee:
        statement = select(Employee).where(Employee.employee_id == employee_id)
        db_employee = self.__session.exec(statement).one_or_none()
        if db_employee is None:
            raise EmployeeNotFoundException(employee_id=employee_id)
        return db_employee

    def create_employee(self, employee: EmployeeCreateUpdate) -> Employee:
        db_employee = Employee(**employee.model_dump())
        try:
            self.__session.add(db_employee)
            self.__session.commit()
            self.__session.refresh(db_employee)
        except IntegrityError as err:
            raise InvalidEmployeeDataException(employee_id=employee.employee_id, error=str(err))
        return db_employee

    def update_employee(self, employee_id: uuid.UUID, employee: EmployeeCreateUpdate) -> Employee:
        db_employee = self.get_employee_by_id(employee_id)
        try:
            db_employee.sqlmodel_update(employee.model_dump())
            self.__session.commit()
            self.__session.refresh(db_employee)
        except IntegrityError as err:
            raise InvalidEmployeeDataException(employee_id=employee_id, error=str(err))
        return db_employee

    def delete_employee(self, employee_id: uuid.UUID) -> None:
        db_employee = self.get_employee_by_id(employee_id)
        try:
            self.__session.delete(db_employee)
            self.__session.commit()
        except IntegrityError as err:
            raise InvalidEmployeeDataException(employee_id=employee_id, error=str(err))
        return None
