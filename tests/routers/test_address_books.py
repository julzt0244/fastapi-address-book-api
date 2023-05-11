class TestAccount:

    test_address_book_name = "Test AddressBook"

    def test_create_address_book_valid_details_should_pass(self, test_client, get_authed_user_1_headers):

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

    def test_create_address_book_duplicate_name_should_fail(self, test_client, get_authed_user_1_headers):

        response = test_client.post(
            "/address-books/",
            json={"name": self.test_address_book_name},
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 409

    def test_read_address_books_authed_user_should_pass(self, test_client, get_authed_user_1_headers):

        response = test_client.get(
            "/address-books/",
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 200
        assert response.json() == [
            {"name": self.test_address_book_name, "id": 1, "contacts": []},
        ]

    def test_read_address_books_unknown_user_should_fail(self, test_client):

        response = test_client.get(
            "/address-books/",
            headers={},
        )
        assert response.status_code == 401

    def test_read_address_book_valid_details_should_pass(self, test_client, get_authed_user_1_headers):

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

    def test_read_address_book_invalid_id_should_fail(self, test_client, get_authed_user_1_headers):

        response = test_client.get(
            "/address-books/9999",
            headers=get_authed_user_1_headers,
        )
        assert response.status_code == 404

    def test_read_address_book_unknown_user_should_fail(self, test_client):

        response = test_client.get(
            "/address-books/1",
            headers={},
        )
        assert response.status_code == 401
