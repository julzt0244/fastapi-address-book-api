import json
import os
from datetime import timedelta

from fastapi.testclient import TestClient
from freezegun import freeze_time

from address_book.auth import ACCESS_TOKEN_EXPIRE_DAYS


class TestAccount:
    test_username = "testuser"
    test_password = "testpassword"

    def test_can_create_user(self, test_client: TestClient):
        response = test_client.post(
            "/account/",
            json={"username": self.test_username, "password": self.test_password},
        )
        assert response.status_code == 200
        assert response.text
        data = response.json()
        assert data["username"] == self.test_username
        assert "id" in data

    def test_cannot_create_duplicate_user(self, test_client: TestClient):
        response = test_client.post(
            "/account/",
            json={"username": self.test_username, "password": self.test_password},
        )
        assert response.status_code == 409

    def test_cannot_login_with_incorrect_credentials(self, test_client: TestClient):
        response = test_client.post(
            "/account/session/",
            data={"username": self.test_username, "password": "WRONGPASSWORD"},
        )
        assert response.status_code == 401

    def test_can_login_with_correct_credentials(self, test_client: TestClient):
        response = test_client.post(
            "/account/session/",
            data={"username": self.test_username, "password": self.test_password},
        )
        assert response.status_code == 200
        data = response.json()
        os.environ["TEST_ACCESS_TOKEN"] = json.dumps(
            {"Authorization": "Bearer " + data["access_token"]}
        )  # Simple persistence for access token

    def test_can_get_own_account_info(self, test_client: TestClient):
        response = test_client.get(
            "/account/",
            headers=json.loads(os.environ["TEST_ACCESS_TOKEN"]),
        )
        assert response.status_code == 200
        data = response.json()
        assert "addressBooks" in data
        assert isinstance(data["addressBooks"], list)

    def test_cannot_get_account_info_if_not_authenticated(
        self, test_client: TestClient
    ):
        response = test_client.get("/account")
        assert response.status_code == 401

    def test_cannot_get_account_info_if_access_token_expired(
        self, test_client: TestClient
    ):
        with freeze_time() as frozen_datetime:
            # Sometime in the past the user has received the token
            response = test_client.post(
                "/account/session/",
                data={"username": self.test_username, "password": self.test_password},
            )
            assert response.status_code == 200
            data = response.json()

            frozen_datetime.tick(timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS + 1))

            response = test_client.get(
                "/account/",
                headers={"Authorization": "Bearer " + data["access_token"]},
            )
            assert response.status_code == 401

    def test_can_delete_own_account(self, test_client: TestClient):
        response = test_client.delete(
            "/account/",
            headers=json.loads(os.environ["TEST_ACCESS_TOKEN"]),
        )
        assert response.status_code == 204
