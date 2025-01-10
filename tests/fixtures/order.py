import pytest
from sqlmodel import Session

from app.api.order import Order, OrderCreate, OrderDataAccessLayer
from app.api.book import Book
from app.api.customer import Customer
from app.api.employee import Employee


@pytest.fixture(scope="session")
def orders_dal(
        test_database_session: Session,
) -> OrderDataAccessLayer:
    return OrderDataAccessLayer(
        session=test_database_session,
    )


@pytest.fixture(scope="module")
def orders(
        orders_dal: OrderDataAccessLayer,
        books: list[Book],
        customers: list[Customer],
        employees: list[Employee],
) -> list[Order]:
    sample_orders = [
        Order(
            customer_id=customers[i].customer_id,
            book_id=books[i].book_id,
            employee_id=employees[i].employee_id,
        ) for i in range(2)
    ]
    for order in sample_orders:
        orders_dal.create_order(order)
    return sample_orders


@pytest.fixture(scope="function")
def order(
        orders_dal: OrderDataAccessLayer,
        books: list[Book],
        customers: list[Customer],
        employees: list[Employee],
) -> Order:
    order = Order(
        customer_id=customers[0].customer_id,
        book_id=books[0].book_id,
        employee_id=employees[0].employee_id,
    )
    orders_dal.create_order(order)
    return order


@pytest.fixture(scope="module")
def create_order_request(
        books: list[Book],
        customers: list[Customer],
        employees: list[Employee],
) -> OrderCreate:
    return OrderCreate(
        customer_id=customers[0].customer_id,
        book_id=books[1].book_id,
        employee_id=employees[0].employee_id,
    )
