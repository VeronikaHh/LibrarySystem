import uuid

import pytest

from app.api.employee import (
    Employee,
    EmployeeUpdate,
    EmployeeDataAccessLayer,
    EmployeeNotFoundException,
    EmployeeCreate,
)


def test_get_all_employees(employees_dal: EmployeeDataAccessLayer, employees: list[Employee]) -> None:
    result = employees_dal.get_all_employees()
    assert len(result) == len(employees)
    for item in result:
        assert isinstance(item, Employee)


def test_get_employee_by_id(employees_dal: EmployeeDataAccessLayer, employees: list[Employee]) -> None:
    retrieved_employee = employees_dal.get_employee_by_id(employees[0].employee_id)
    assert retrieved_employee is not None
    assert isinstance(retrieved_employee, Employee)
    assert retrieved_employee.name == employees[0].name
    assert retrieved_employee.email == employees[0].email
    assert retrieved_employee.phone_number == employees[0].phone_number


def test_get_employee_by_id_not_found(employees_dal: EmployeeDataAccessLayer, employees: list[Employee]) -> None:
    with pytest.raises(EmployeeNotFoundException):
        employees_dal.get_employee_by_id(uuid.uuid4())


def test_create_employee(employees_dal: EmployeeDataAccessLayer, create_employee_request: EmployeeCreate) -> None:
    created_employee = employees_dal.create_employee(employee=create_employee_request)
    assert created_employee is not None
    assert created_employee.name == create_employee_request.name
    assert created_employee.email == create_employee_request.email


def test_update_employee(employees_dal: EmployeeDataAccessLayer, employees: list[Employee]) -> None:
    updated_employee = employees_dal.update_employee(
        employee_id=employees[0].employee_id,
        employee=EmployeeUpdate(email="updated_email@mail.com"),
    )
    assert updated_employee.email == "updated_email@mail.com"


def test_delete_employee(employees_dal: EmployeeDataAccessLayer, employee_without_orders: Employee) -> None:
    employees_dal.delete_employee(employee_id=employee_without_orders.employee_id)
    with pytest.raises(EmployeeNotFoundException):
        employees_dal.get_employee_by_id(employee_without_orders.employee_id)
