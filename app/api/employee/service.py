import uuid
from typing import Annotated

from fastapi import Depends

from .dal import EmployeeDataAccessLayer
from .models import Employee, EmployeeUpdate, EmployeeCreate


class EmployeeService:
    def __init__(
            self,
            employee_dal: Annotated[EmployeeDataAccessLayer, Depends()],
    ) -> None:
        self.employee_dal = employee_dal

    def get_all_employees(self) -> list[Employee]:
        return list(self.employee_dal.get_all_employees())

    def get_employee_by_id(self, employee_id: uuid.UUID) -> Employee:
        return self.employee_dal.get_employee_by_id(employee_id)

    def create_employee(self, employee: EmployeeCreate) -> Employee:
        return self.employee_dal.create_employee(employee)

    def update_employee(self, employee_id: uuid.UUID, employee: EmployeeUpdate) -> Employee:
        return self.employee_dal.update_employee(employee_id, employee)

    def delete_employee(self, employee_id: uuid.UUID) -> None:
        return self.employee_dal.delete_employee(employee_id)
