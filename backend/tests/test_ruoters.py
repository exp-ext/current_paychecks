import time

import pytest
from fastapi.testclient import TestClient


class TestBlog:
    USER = {
        "username": f"testuser{int(time.time())}",
        "password": "testpassword"
    }
    USER_EMPLOYEE = {
        "username": f"testuser_employee{int(time.time())}",
        "password": "testpassword_employee"
    }

    def get_auth_client(self, client: TestClient) -> TestClient:
        response = client.post("/api/auth/login/", json=self.USER)
        access_token = response.json()["access_token"]
        return TestClient(
            client.app, headers={"Authorization": f"Bearer {access_token}"}
        )

    def get_auth_client_employee(self, client: TestClient) -> TestClient:
        response = client.post("/api/auth/login/", json=self.USER_EMPLOYEE)
        access_token = response.json()["access_token"]
        return TestClient(
            client.app, headers={"Authorization": f"Bearer {access_token}"}
        )

    def test_register(self, client: TestClient, db):
        for user in [self.USER, self.USER_EMPLOYEE]:
            response = client.post("/api/auth/register/", json=user)
            assert response.status_code == 201
            assert response.json()["username"] == user.get("username")

    def test_login(self, client: TestClient) -> TestClient:
        response = client.post("/api/auth/login/", json=self.USER_EMPLOYEE)
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "Bearer"

    def test_get_staff(self, client: TestClient, db):
        code = {"code": "надо"}
        response = self.get_auth_client(client).patch(
            "/api/auth/users/get-staff-status/", json=code
        )
        assert response.status_code == 200
        assert response.json()["Status Staff"] is True

    @pytest.mark.parametrize("skip, limit", [(0, 20), (0, 1)])
    def test_read_users(self, client: TestClient, db, skip, limit):
        response = self.get_auth_client(client).get(
            f"/api/auth/users/?skip={skip}&limit={limit}"
        )
        assert response.status_code == 200
        users = response.json()
        assert len(users) <= limit

    def test_read_user(self, client: TestClient, db):
        response = self.get_auth_client(client).get("/api/auth/users/me/")
        assert response.status_code == 200
        response = client.get("/api/auth/users/me/")
        assert response.status_code == 401

    def test_set_rate(self, client: TestClient, db):
        salary = {
            "employee_id": 2,
            "current_rate": 50000,
            "rate_increase_period": 90
        }
        response = self.get_auth_client(client).post(
            "/api/salary/set-rate/", json=salary
        )
        assert response.status_code == 201
        assert float(response.json()['current_rate'])
        assert response.json()['current_rate'] == 50000.0
        assert response.json()['employee_id'] == 2

        response = client.post(
            "/api/salary/set-rate/", json=salary
        )
        assert response.status_code == 401

    def test_next_pay_raise(self, client: TestClient, db):
        response = self.get_auth_client_employee(client).get(
            "/api/next-pay-raise"
        )
        assert response.status_code == 404
