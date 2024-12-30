import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status

from .dal import EmployeeDataAccessLayer
from .models import Employee, EmployeeCreate, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["Employee"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_employees(employee_dal: Annotated[EmployeeDataAccessLayer, Depends()]) -> list[Employee]:
    return list(employee_dal.get_all_employees())


@router.get("/{employee_id}", status_code=status.HTTP_200_OK)
async def get_employee_by_id(employee_id: uuid.UUID,
                             employee_dal: Annotated[EmployeeDataAccessLayer, Depends()]) -> Employee:
    return employee_dal.get_employee_by_id(employee_id=employee_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate,
                          employee_dal: Annotated[EmployeeDataAccessLayer, Depends()]) -> Employee:
    return employee_dal.create_employee(employee=employee)


@router.put("/{employee_id}", status_code=status.HTTP_200_OK)
async def update_employee(
        employee_id: uuid.UUID,
        employee: EmployeeUpdate,
        employee_dal: Annotated[EmployeeDataAccessLayer, Depends()],
) -> Employee:
    return employee_dal.update_employee(employee_id=employee_id, employee=employee)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: uuid.UUID, employee_dal: Annotated[EmployeeDataAccessLayer, Depends()]) -> None:
    return employee_dal.delete_employee(employee_id=employee_id)
