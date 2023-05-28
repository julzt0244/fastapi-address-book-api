import json
import os

from fastapi.testclient import TestClient


class TestContacts:
    test_address_book_name_1 = "Work Profile"
    test_address_book_id_1: int = 1
    test_address_book_name_2 = "Personal Profile"
    test_address_book_id_2: int = 2
    test_contact_name: str = "Peter Smith"
    test_contact_phone_number: str = "0412341234"

    def test_can_create_contact(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        response_create_address_book = test_client.post(
            "/address-books/",
            json={"name": self.test_address_book_name_1},
            headers=get_authed_user_1_headers,
        )
        assert response_create_address_book.status_code == 200
        response_create_address_book.json()

        response_create_contact = test_client.post(
            "/contacts/",
            json={
                "name": self.test_contact_name,
                "phoneNumber": self.test_contact_phone_number,
                "addressBookId": self.test_address_book_id_1,
            },
            headers=get_authed_user_1_headers,
        )
        assert response_create_contact.status_code == 200
        assert response_create_contact.json() == {
            "name": self.test_contact_name,
            "phoneNumber": self.test_contact_phone_number,
            "id": 1,
            "addressBookId": self.test_address_book_id_1,
        }

    def test_cannot_create_contact_for_other_users_address_book(
        self, test_client: TestClient, get_authed_user_2_headers: dict[str, str]
    ):
        """
        Check that a user can only create contacts in their own address books
        """
        response_create_contact = test_client.post(
            "/contacts/",
            json={
                "name": self.test_contact_name,
                "phoneNumber": self.test_contact_phone_number,
                "addressBookId": self.test_address_book_id_1,
            },
            headers=get_authed_user_2_headers,
        )
        assert response_create_contact.status_code == 404

    def test_cannot_create_contact_if_not_authenticated(self, test_client: TestClient):
        response = test_client.post(
            "/contacts/",
            json={
                "name": self.test_contact_name,
                "phoneNumber": self.test_contact_phone_number,
                "addressBookId": self.test_address_book_id_1,
            },
            headers={},
        )
        assert response.status_code == 401

    def test_can_get_combined_list_of_contacts(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        # SETUP
        # Create second address book
        response_create_address_book = test_client.post(
            "/address-books/",
            json={"name": self.test_address_book_name_2},
            headers=get_authed_user_1_headers,
        )
        assert response_create_address_book.status_code == 200

        # Create second contact which has the same details as the first contact, but will be done in another address book id
        response_create_contact = test_client.post(
            "/contacts/",
            json={
                "name": self.test_contact_name,
                "phoneNumber": self.test_contact_phone_number,
                "addressBookId": self.test_address_book_id_2,
            },
            headers=get_authed_user_1_headers,
        )
        assert response_create_contact.status_code == 200

        # TEST
        response_get_contacts = test_client.get(
            "/contacts/",
            headers=get_authed_user_1_headers,
        )
        assert response_get_contacts.status_code == 200
        assert response_get_contacts.json() == [
            {
                "name": self.test_contact_name,
                "phoneNumber": self.test_contact_phone_number,
            },
            {
                "name": self.test_contact_name,
                "phoneNumber": self.test_contact_phone_number,
            },
        ]

    def test_can_get_unique_list_of_contacts(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        response = test_client.get(
            "/contacts/?unique=true",
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 200
        assert response.json() == [
            {
                "name": self.test_contact_name,
                "phoneNumber": self.test_contact_phone_number,
            },
        ]

    def test_can_read_contact_details(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        response = test_client.get(
            "/contacts/1/",
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": self.test_contact_name,
            "phoneNumber": self.test_contact_phone_number,
            "id": 1,
            "addressBookId": self.test_address_book_id_1,
        }

    def test_with_non_existant_contact(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        response = test_client.get(
            "/contacts/999/",
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 404

    def test_cannot_access_other_users_contacts(self, test_client):
        # SETUP
        # Create second authed user
        response_create_account = test_client.post(
            "/account/",
            json={"username": "hellohello", "password": "hellohello"},
        )
        assert response_create_account.status_code == 200
        response_login = test_client.post(
            "/account/session/",
            data={"username": "hellohello", "password": "hellohello"},
        )
        assert response_login.status_code == 200
        headers_second_user: dict[str, str] = {
            "Authorization": "Bearer " + response_login.json()["access_token"]
        }
        os.environ["TEST_ACCESS_TOKEN_2"] = json.dumps(headers_second_user)

        # TEST
        response = test_client.get(
            "/contacts/1/",
            headers=headers_second_user,
        )
        assert response.status_code == 403

    def test_can_delete_own_contacts(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        response = test_client.delete(
            "/contacts/1",
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 204
        assert response.content.decode() == ""

    def test_when_deleting_non_existant_contact(
        self, test_client: TestClient, get_authed_user_1_headers: dict[str, str]
    ):
        response = test_client.delete(
            "/contacts/999",
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 404

    def test_cannot_delete_other_users_contacts(self, test_client):
        response = test_client.delete(
            "/contacts/2",
            headers=json.loads(os.environ["TEST_ACCESS_TOKEN_2"]),
        )
        assert response.status_code == 403
