import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status

from .dal import CustomerDataAccessLayer
from .models import Customer, CustomerCreate, CustomerUpdate

router = APIRouter(prefix="/customers", tags=["Customer"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_customers(customer_dal: Annotated[CustomerDataAccessLayer, Depends()]) -> list[Customer]:
    return list(customer_dal.get_all_customers())


@router.get("/{customer_id}", status_code=status.HTTP_200_OK)
async def get_customer_by_id(customer_id: uuid.UUID,
                             customer_dal: Annotated[CustomerDataAccessLayer, Depends()]) -> Customer:
    return customer_dal.get_customer_by_id(customer_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreate,
                          customer_dal: Annotated[CustomerDataAccessLayer, Depends()]) -> Customer:
    return customer_dal.create_customer(customer=customer)


@router.put("/{customer_id}", status_code=status.HTTP_200_OK)
async def update_customer(
        customer_id: uuid.UUID,
        customer: CustomerUpdate,
        customer_dal: Annotated[CustomerDataAccessLayer, Depends()],
) -> Customer:
    return customer_dal.update_customer(customer_id=customer_id, customer=customer)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: uuid.UUID, customer_dal: Annotated[CustomerDataAccessLayer, Depends()]) -> None:
    return customer_dal.delete_customer(customer_id=customer_id)
