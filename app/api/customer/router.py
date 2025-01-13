import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status

from .service import CustomerService
from .models import Customer, CustomerCreate, CustomerUpdate

router = APIRouter(prefix="/customers", tags=["Customer"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_customers(customer_service: Annotated[CustomerService, Depends()]) -> list[Customer]:
    return list(customer_service.get_all_customers())


@router.get("/{customer_id}", status_code=status.HTTP_200_OK)
async def get_customer_by_id(customer_id: uuid.UUID,
                             customer_service: Annotated[CustomerService, Depends()]) -> Customer:
    return customer_service.get_customer_by_id(customer_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreate,
                          customer_service: Annotated[CustomerService, Depends()]) -> Customer:
    return customer_service.create_customer(customer=customer)


@router.put("/{customer_id}", status_code=status.HTTP_200_OK)
async def update_customer(
        customer_id: uuid.UUID,
        customer: CustomerUpdate,
        customer_service: Annotated[CustomerService, Depends()],
) -> Customer:
    return customer_service.update_customer(customer_id=customer_id, customer=customer)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: uuid.UUID, customer_service: Annotated[CustomerService, Depends()]) -> None:
    return customer_service.delete_customer(customer_id=customer_id)
