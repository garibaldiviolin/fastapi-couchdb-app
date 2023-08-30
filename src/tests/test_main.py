from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_item(existing_item):
    response = client.get("/items/81238/")
    assert response.status_code == 200
    assert response.json() == existing_item
