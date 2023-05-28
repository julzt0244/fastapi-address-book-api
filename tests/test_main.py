from fastapi.testclient import TestClient

from address_book.main import app

test_client = TestClient(app)


def test_can_browse_root_page():
    response = test_client.get("/")
    assert response.status_code == 200
