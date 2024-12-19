import uuid
from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db_config import get_database_session
from .models import Customer

router = APIRouter(prefix="/customers",tags=["Customer"])


@router.get("", status_code=200)
async def get_customers(session: Annotated[Session, Depends(get_database_session)]):
    customers = session.exec(select(Customer)).all()
    return customers

@router.get("/{customer_id}", status_code=200)
async def get_customer_by_id(customer_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise HTTPException()
    return customer

@router.post("", status_code=201)
async def create_customer(customer: Customer, session: Annotated[Session, Depends(get_database_session)]):
    db_customer = Customer(**customer.model_dump())
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer

@router.put("/{customer_id}", status_code=201)
async def update_customer(customer_id: uuid.UUID, customer: Customer, session: Annotated[Session, Depends(get_database_session)]):
    db_customer = session.get(Customer, customer_id)
    if db_customer is None:
        raise HTTPException()
    db_customer.sqlmodel_update(customer.model_dump())
    session.commit()
    session.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}", status_code=200)
async def delete_customer(customer_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException()
    session.delete(customer)
    session.commit()
    return {"ok": True}