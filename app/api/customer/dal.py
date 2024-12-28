import uuid
from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.db_config import get_database_session
from .exceptions import CustomerNotFoundException, InvalidCustomerDataException
from .models import Customer, CustomerCreateUpdate


class CustomerDataAccessLayer:
    def __init__(self, session: Annotated[Session, Depends(get_database_session)]):
        self.__session = session

    def get_all_customers(self) -> Sequence[Customer]:
        db_customers = self.__session.exec(select(Customer)).all()
        return db_customers

    def get_customer_by_id(self, customer_id: uuid.UUID) -> Customer:
        statement = select(Customer).where(Customer.id == customer_id)
        db_customer = self.__session.exec(statement).one_or_none()
        if db_customer is None:
            raise CustomerNotFoundException(customer_id=customer_id)
        return db_customer

    def create_customer(self, customer: CustomerCreateUpdate) -> Customer:
        db_customer = Customer(**customer.model_dump())
        try:
            self.__session.add(db_customer)
            self.__session.commit()
            self.__session.refresh(db_customer)
        except IntegrityError as err:
            raise InvalidCustomerDataException(customer_id=customer.customer_id, error=str(err))
        return db_customer

    def update_customer(self, customer_id: uuid.UUID, customer: CustomerCreateUpdate) -> Customer:
        db_customer = self.get_customer_by_id(customer_id)
        try:
            db_customer.sqlmodel_update(customer.model_dump())
            self.__session.commit()
            self.__session.refresh(db_customer)
        except IntegrityError as err:
            raise InvalidCustomerDataException(customer_id=customer_id, error=str(err))
        return db_customer

    def delete_customer(self, customer_id: uuid.UUID) -> None:
        db_customer = self.get_customer_by_id(customer_id)
        try:
            self.__session.delete(db_customer)
            self.__session.commit()
        except IntegrityError as err:
            raise InvalidCustomerDataException(customer_id=customer_id, error=str(err))
        return None
