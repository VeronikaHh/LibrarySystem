import uuid

from fastapi.testclient import TestClient

from app.api.employee import Employee, EmployeeCreate


def test_get_all_employees(test_client: TestClient) -> None:
    response = test_client.get("/employees")
    assert response.status_code == 200


def test_get_employee_by_id(test_client: TestClient, employees: list[Employee]) -> None:
    employee_id = employees[0].employee_id
    response = test_client.get(f"/employees/{employee_id}")
    assert response.status_code == 200


def test_get_employee_by_id_not_exist(test_client: TestClient) -> None:
    employee_id = uuid.uuid4()
    response = test_client.get(f"/employees/{employee_id}")
    assert response.status_code == 404


def test_create_employee(test_client: TestClient, create_employee_request: EmployeeCreate) -> None:
    response = test_client.post("/employees", json=create_employee_request.model_dump())
    assert response.status_code == 201


def test_update_employee(test_client: TestClient, employees: list[Employee]) -> None:
    employee_id = employees[0].employee_id
    response = test_client.put(f"/employees/{employee_id}", json={})
    assert response.status_code == 200


def test_update_employee_not_exist(test_client: TestClient) -> None:
    employee_id = uuid.uuid4()
    response = test_client.put(f"/employees/{employee_id}", json={})
    assert response.status_code == 404


def test_delete_employee(test_client: TestClient, employee_without_orders: Employee) -> None:
    employee_id = employee_without_orders.employee_id
    response = test_client.delete(f"/employees/{employee_id}")
    assert response.status_code == 204


def test_delete_employee_not_exist(test_client: TestClient) -> None:
    employee_id = uuid.uuid4()
    response = test_client.delete(f"/employees/{employee_id}")
    assert response.status_code == 404
