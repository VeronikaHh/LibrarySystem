import uuid

import pytest
from sqlmodel import Session

from app.api.employee import Employee, EmployeeDataAccessLayer, EmployeeCreate


@pytest.fixture(scope="session")
def employees_dal(
        test_database_session: Session,
) -> EmployeeDataAccessLayer:
    return EmployeeDataAccessLayer(
        session=test_database_session,
    )


@pytest.fixture(scope="module")
def employees(employees_dal: EmployeeDataAccessLayer) -> list[Employee]:
    sample_employees = [
        Employee(
            name="Admin Employee",
            email=str(uuid.uuid4()),
            phone_number=str(uuid.uuid4()),
            address = "Employee One address",
            is_admin=True,
        ),
        Employee(
            name="Employee One",
            email=str(uuid.uuid4()),
            phone_number=str(uuid.uuid4()),
            address = "Employee One address",
            is_admin=False,
        ),
        Employee(
            name="Employee Two",
            email=str(uuid.uuid4()),
            phone_number=str(uuid.uuid4()),
            address = "Employee One address",
            is_admin=False,
        ),
    ]
    for employee in sample_employees:
        employees_dal.create_employee(employee)
    return sample_employees


@pytest.fixture(scope="module")
def create_employee_request() -> EmployeeCreate:
    return EmployeeCreate(
        name="Test Employee",
        email=str(uuid.uuid4()),
        phone_number=str(uuid.uuid4()),
        address = "Test Employee address",
        is_admin=False,
    )
