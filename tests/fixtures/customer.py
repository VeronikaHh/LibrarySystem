import uuid

import pytest
from sqlmodel import Session

from app.api.customer import Customer, CustomerDataAccessLayer, CustomerCreate, CustomerService


@pytest.fixture(scope="session")
def customers_dal(
        test_database_session: Session,
) -> CustomerDataAccessLayer:
    return CustomerDataAccessLayer(
        session=test_database_session,
    )


@pytest.fixture(scope="session")
def customers_service(
        customers_dal: CustomerDataAccessLayer,
) -> CustomerService:
    return CustomerService(customers_dal=customers_dal)


@pytest.fixture(scope="module")
def customers(customers_dal: CustomerDataAccessLayer) -> list[Customer]:
    old_customers = customers_dal.get_all_customers()
    for customer in old_customers:
        customers_dal.delete_customer(customer.customer_id)

    sample_customers = [
        Customer(name="Customer One", email=str(uuid.uuid4()), phone_number=str(uuid.uuid4()), is_ower=False),
        Customer(name="Customer Two", email=str(uuid.uuid4()), phone_number=str(uuid.uuid4()), is_ower=False),
    ]
    for customer in sample_customers:
        customers_dal.create_customer(customer)
    return sample_customers


@pytest.fixture(scope="module")
def create_customer_request() -> CustomerCreate:
    return CustomerCreate(name="Test Customer", email=str(uuid.uuid4()), phone_number=str(uuid.uuid4()), is_ower=False)


@pytest.fixture(scope="module")
def customers_with_orders(customers_dal: CustomerDataAccessLayer) -> list[Customer]:
    sample_customers = [
        Customer(name="Customer One", email=str(uuid.uuid4()), phone_number=str(uuid.uuid4()), is_ower=False),
        Customer(name="Customer Two", email=str(uuid.uuid4()), phone_number=str(uuid.uuid4()), is_ower=False),
    ]
    for customer in sample_customers:
        customers_dal.create_customer(customer)
    return sample_customers

@pytest.fixture(scope="module")
def customer_without_orders(customers_dal: CustomerDataAccessLayer) -> list[Customer]:
    customer = Customer(
        name="Customer No Orders",
        email=str(uuid.uuid4()),
        phone_number=str(uuid.uuid4()),
        is_ower=False,
    )
    customers_dal.create_customer(customer)
    return customer


@pytest.fixture(scope="module")
def customer(customers_dal: CustomerDataAccessLayer) -> Customer:
    customer = Customer(name="Valid Customer", email=str(uuid.uuid4()), phone_number=str(uuid.uuid4()), is_ower=False)
    customers_dal.create_customer(customer)
    return customer


@pytest.fixture(scope="module")
def customer_is_ower(customers_dal: CustomerDataAccessLayer) -> Customer:
    customer = Customer(name="Customer", email=str(uuid.uuid4()), phone_number=str(uuid.uuid4()), is_ower=True)
    customers_dal.create_customer(customer)
    return customer
