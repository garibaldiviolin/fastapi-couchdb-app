from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_item(existing_item, existing_item_id):
    response = client.get(f"/items/{existing_item_id}/")
    assert response.status_code == 200
    assert response.json() == existing_item
