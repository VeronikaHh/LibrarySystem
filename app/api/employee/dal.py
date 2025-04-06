import uuid
from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.db_config import get_database_session
from .exceptions import (
    EmployeeNotFoundException,
    InvalidEmployeeDataException,
    EmployeeDeleteException,
)
from .models import Employee, EmployeeCreate, EmployeeUpdate, EmployeeResponse


class EmployeeDataAccessLayer:
    def __init__(self, session: Annotated[Session, Depends(get_database_session)]) -> None:
        self.__session = session

    def get_all_employees(self) -> Sequence[EmployeeResponse]:
        employees = self.__session.exec(select(Employee)).all()
        # return [EmployeeResponse.model_validate(emp) for emp in employees]
        return [EmployeeResponse(**emp.model_dump()) for emp in employees]

    def get_employee_by_id(self, employee_id: uuid.UUID) -> EmployeeResponse:
        statement = select(Employee).where(Employee.employee_id == employee_id)
        db_employee = self.__session.exec(statement).one_or_none()
        if db_employee is None:
            raise EmployeeNotFoundException(employee_id=employee_id)
        return EmployeeResponse(**db_employee.model_dump())

    def create_employee(self, employee: EmployeeCreate) -> EmployeeResponse:
        # Create employee WITHOUT password first
        employee_data = employee.model_dump(exclude={"password"})
        db_employee = Employee(**employee_data)

        # Set the hashed password separately
        db_employee.set_password(employee.password)
        try:
            self.__session.add(db_employee)
            self.__session.commit()
            self.__session.refresh(db_employee)
        except IntegrityError as err:
            raise InvalidEmployeeDataException(employee_id=employee.employee_id, error=str(err))
        return EmployeeResponse(**db_employee.model_dump())

    def update_employee(self, employee_id: uuid.UUID, employee: EmployeeUpdate) -> EmployeeResponse:
        db_employee = self.get_employee_by_id(employee_id)
        try:
            db_employee.sqlmodel_update(employee.model_dump(exclude_none=True))
            self.__session.commit()
            self.__session.refresh(db_employee)
        except IntegrityError as err:
            raise InvalidEmployeeDataException(employee_id=employee_id, error=str(err))
        return EmployeeResponse(**db_employee.model_dump())

    def delete_employee(self, employee_id: uuid.UUID) -> None:
        db_employee = self.get_employee_by_id(employee_id)
        try:
            self.__session.delete(db_employee)
            self.__session.commit()
        except IntegrityError as err:
            raise EmployeeDeleteException(employee_id=employee_id, error=str(err))

    def update_password(self, employee_id: uuid.UUID, new_password: str) -> EmployeeResponse:
        db_employee = self.get_employee_by_id(employee_id)
        db_employee.set_password(new_password)
        try:
            self.__session.commit()
            self.__session.refresh(db_employee)
        except IntegrityError as err:
            raise InvalidEmployeeDataException(employee_id=employee_id, error=str(err))
        return EmployeeResponse(**db_employee.model_dump())
