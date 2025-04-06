import uuid
from typing import Annotated

from fastapi import Depends

from .dal import EmployeeDataAccessLayer
from .models import EmployeeUpdate, EmployeeCreate, EmployeeResponse


class EmployeeService:
    def __init__(
            self,
            employees_dal: Annotated[EmployeeDataAccessLayer, Depends()],
    ) -> None:
        self.employees_dal = employees_dal

    def get_all_employees(self) -> list[EmployeeResponse]:
        return list(self.employees_dal.get_all_employees())

    def get_employee_by_id(self, employee_id: uuid.UUID) -> EmployeeResponse:
        return self.employees_dal.get_employee_by_id(employee_id)

    def create_employee(self, employee: EmployeeCreate) -> EmployeeResponse:
        return self.employees_dal.create_employee(employee)

    def update_employee(self, employee_id: uuid.UUID, employee: EmployeeUpdate) -> EmployeeResponse:
        return self.employees_dal.update_employee(employee_id, employee)

    def delete_employee(self, employee_id: uuid.UUID) -> None:
        return self.employees_dal.delete_employee(employee_id)
