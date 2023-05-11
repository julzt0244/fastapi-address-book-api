import json
import os

from fastapi.testclient import TestClient


class TestAccount:
    test_username = "testuser"
    test_password = "testpassword"

    def test_create_user_new_user_should_pass(self, test_client: TestClient):
        response = test_client.post(
            "/account/",
            json={"username": self.test_username, "password": self.test_password},
        )
        assert response.status_code == 200
        assert response.text
        data = response.json()
        assert data["username"] == self.test_username
        assert "id" in data

    def test_create_user_duplicate_user_should_fail(self, test_client: TestClient):
        response = test_client.post(
            "/account/",
            json={"username": self.test_username, "password": self.test_password},
        )
        assert response.status_code == 409

    def test_login_user_invalid_details_should_fail(self, test_client: TestClient):
        response = test_client.post(
            "/account/session/",
            data={"username": self.test_username, "password": "WRONGPASSWORD"},
        )
        assert response.status_code == 401

    def test_login_user_valid_details_should_pass(self, test_client: TestClient):
        response = test_client.post(
            "/account/session/",
            data={"username": self.test_username, "password": self.test_password},
        )
        assert response.status_code == 200
        data = response.json()
        os.environ["TEST_ACCESS_TOKEN"] = json.dumps(
            {"Authorization": "Bearer " + data["access_token"]}
        )  # Simple persistence for access token

    def test_get_user_account_info_authed_user_should_pass(
        self, test_client: TestClient
    ):
        response = test_client.get(
            "/account/",
            headers=json.loads(os.environ["TEST_ACCESS_TOKEN"]),
        )
        assert response.status_code == 200
        data = response.json()
        assert "addressBooks" in data
        assert isinstance(data["addressBooks"], list)

    def test_get_user_account_info_unknown_user_should_fail(
        self, test_client: TestClient
    ):
        response = test_client.get("/account")
        assert response.status_code == 401

    def test_delete_user_can_delete_own_account_pass(self, test_client: TestClient):
        response = test_client.delete(
            "/account/",
            headers=json.loads(os.environ["TEST_ACCESS_TOKEN"]),
        )
        assert response.status_code == 204
