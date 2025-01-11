import uuid

import pytest
from sqlmodel import Session

from app.api.employee import Employee, EmployeeDataAccessLayer, EmployeeCreate, EmployeeService
from app.api.order import OrderDataAccessLayer


@pytest.fixture(scope="session")
def employees_dal(
        test_database_session: Session,
) -> EmployeeDataAccessLayer:
    return EmployeeDataAccessLayer(
        session=test_database_session,
    )


@pytest.fixture(scope="session")
def employees_service(
        employees_dal: EmployeeDataAccessLayer,
) -> EmployeeService:
    return EmployeeService(employees_dal=employees_dal)


@pytest.fixture(scope="module")
def employees(
        employees_dal: EmployeeDataAccessLayer,
        orders_dal: OrderDataAccessLayer,
) -> list[Employee]:
    old_employees = employees_dal.get_all_employees()
    for employee in old_employees:
        employees_dal.delete_employee(employee.employee_id)

    sample_employees = [
        Employee(
            name="Admin Employee",
            email=str(uuid.uuid4()),
            phone_number=str(uuid.uuid4()),
            address="Employee One address",
            is_admin=True,
        ),
        Employee(
            name="Employee One",
            email=str(uuid.uuid4()),
            phone_number=str(uuid.uuid4()),
            address="Employee One address",
            is_admin=False,
        ),
        Employee(
            name="Employee Two",
            email=str(uuid.uuid4()),
            phone_number=str(uuid.uuid4()),
            address="Employee One address",
            is_admin=False,
        ),
    ]
    for employee in sample_employees:
        employees_dal.create_employee(employee)
    return sample_employees

@pytest.fixture(scope="module")
def employee_with_orders(employees_dal: EmployeeDataAccessLayer) -> Employee:
    employee = Employee(
        name="Employee with orders",
        email=str(uuid.uuid4()),
        phone_number=str(uuid.uuid4()),
        address="Test Employee address",
        is_admin=False,
    )
    employees_dal.create_employee(employee)
    return employee

@pytest.fixture(scope="module")
def create_employee_request() -> EmployeeCreate:
    return EmployeeCreate(
        name="Test Employee",
        email=str(uuid.uuid4()),
        phone_number=str(uuid.uuid4()),
        address="Test Employee address",
        is_admin=False,
    )


@pytest.fixture(scope="function")
def employee_without_orders(employees_dal: EmployeeDataAccessLayer) -> Employee:
    employee = Employee(
        name="Orderless Employee",
        email=str(uuid.uuid4()),
        phone_number=str(uuid.uuid4()),
        address="Test Employee address",
        is_admin=False,
    )
    employees_dal.create_employee(employee)
    return employee
