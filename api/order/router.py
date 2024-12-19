import uuid
from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db_config import get_database_session
from .models import Order

router = APIRouter(prefix="/orders",tags=["Order"])


@router.get("", status_code=200)
async def get_orders(session: Annotated[Session, Depends(get_database_session)]):
    orders = session.exec(select(Order)).all()
    return orders

@router.get("/{order_id}", status_code=200)
async def get_order_by_id(order_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    order = session.get(Order, order_id)
    if order is None:
        raise HTTPException()
    return order

@router.post("", status_code=201)
async def create_order(order: Order, session: Annotated[Session, Depends(get_database_session)]):
    db_order = Order(**order.model_dump())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.put("/{order_id}", status_code=201)
async def update_order(order_id: uuid.UUID, order: Order, session: Annotated[Session, Depends(get_database_session)]):
    db_order = session.get(Order, order_id)
    if db_order is None:
        raise HTTPException()

    db_order.sqlmodel_update(order.model_dump())
    session.commit()
    session.refresh(db_order)
    return db_order

@router.delete("/{order_id}", status_code=200)
async def delete_order(order_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException()
    session.delete(order)
    session.commit()
    return {"ok": True}