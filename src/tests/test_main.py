from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_item():
    response = client.get("/items/2/")
    assert response.status_code == 200
    assert response.json() == {
        "_id": "items:2", "_rev": "4-03b50752305d4c5b63c2ae45666c28df", "title": "Granny's cookies", "rating": "123", "name": "soap3", "description": None, "price": 1.54
    }
