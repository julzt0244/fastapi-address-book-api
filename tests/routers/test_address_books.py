from fastapi.testclient import TestClient


class TestAddressBook:
    test_address_book_name = "Test AddressBook"

    def test_can_create_address_book(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        response = test_client.post(
            "/address-books/",
            json={"name": self.test_address_book_name},
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": self.test_address_book_name,
            "id": 1,
            "contacts": [],
        }

    def test_cannot_create_duplicate_address_book_name(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        response = test_client.post(
            "/address-books/",
            json={"name": self.test_address_book_name},
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 409

    def test_can_get_address_books(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        response = test_client.get(
            "/address-books/",
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 200
        assert response.json() == [
            {"name": self.test_address_book_name, "id": 1, "contacts": []},
        ]

    def test_cannot_get_address_books_if_not_authenticated(
        self, test_client: TestClient
    ):
        response = test_client.get(
            "/address-books/",
            headers={},
        )
        assert response.status_code == 401

    def test_can_get_address_book_details(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        response = test_client.get(
            "/address-books/1",
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": self.test_address_book_name,
            "id": 1,
            "contacts": [],
        }

    def test_when_accessing_non_existant_address_book_details(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        response = test_client.get(
            "/address-books/9999",
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 404

    def test_cannot_get_address_book_details_if_not_authenticated(
        self, test_client: TestClient
    ):
        response = test_client.get(
            "/address-books/1",
            headers={},
        )
        assert response.status_code == 401
