import uuid
from typing import Annotated

from fastapi import Depends

from .exceptions import CustomerIsOwerException, CustomerReachedOrderLimitException
from .dal import CustomerDataAccessLayer
from .models import Customer, CustomerUpdate, CustomerCreate


class   CustomerService:
    def __init__(
            self,
            customers_dal: Annotated[CustomerDataAccessLayer, Depends()],
    ) -> None:
        self.customers_dal = customers_dal

    def get_all_customers(self) -> list[Customer]:
        return list(self.customers_dal.get_all_customers())

    def get_customer_by_id(self, customer_id: uuid.UUID) -> Customer:
        return self.customers_dal.get_customer_by_id(customer_id)

    def create_customer(self, customer: CustomerCreate) -> Customer:
        return self.customers_dal.create_customer(customer)

    def update_customer(self, customer_id: uuid.UUID, customer: CustomerUpdate) -> Customer:
        return self.customers_dal.update_customer(customer_id, customer)

    def delete_customer(self, customer_id: uuid.UUID) -> None:
        return self.customers_dal.delete_customer(customer_id)

    def customer_check(self, customer_id: uuid.UUID, orders_quantity: int) -> None:
        db_customer = self.get_customer_by_id(customer_id)
        if db_customer.is_ower:
            raise CustomerIsOwerException(customer_id=customer_id)
        if orders_quantity == 5:
            raise CustomerReachedOrderLimitException(customer_id=customer_id)
