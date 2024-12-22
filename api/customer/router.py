import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from db_config import get_database_session
from .exceptions import CustomerNotFoundError, InvalidCustomerDataError
from .models import Customer, CustomerCreateUpdate

router = APIRouter(prefix="/customers", tags=["Customer"])


@router.get("", status_code=200)
async def get_customers(session: Annotated[Session, Depends(get_database_session)]):
    db_customers = session.exec(select(Customer)).all()
    return db_customers


@router.get("/{customer_id}", status_code=200)
async def get_customer_by_id(customer_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    db_customer = session.get(Customer, customer_id)
    if db_customer is None:
        raise CustomerNotFoundError(customer_id=customer_id)
    return db_customer


@router.post("", status_code=201)
async def create_customer(customer: CustomerCreateUpdate, session: Annotated[Session, Depends(get_database_session)]):
    db_customer = Customer(**customer.model_dump())
    try:
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)
    except IntegrityError as err:
        raise InvalidCustomerDataError(customer_id=customer.customer_id, error=str(err))
    return db_customer


@router.put("/{customer_id}", status_code=201)
async def update_customer(customer_id: uuid.UUID, customer: CustomerCreateUpdate,
                          session: Annotated[Session, Depends(get_database_session)]):
    db_customer = session.get(Customer, customer_id)
    if db_customer is None:
        raise CustomerNotFoundError(customer_id=customer_id)
    try:
        db_customer.sqlmodel_update(customer.model_dump())
        session.commit()
        session.refresh(db_customer)
    except IntegrityError as err:
        raise InvalidCustomerDataError(customer_id=customer.customer_id, error=str(err))
    return db_customer


@router.delete("/{customer_id}", status_code=200)
async def delete_customer(customer_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    db_customer = session.get(Customer, customer_id)
    if not db_customer:
        raise CustomerNotFoundError(customer_id=customer_id)
    session.delete(db_customer)
    session.commit()
    return {"ok": True}
