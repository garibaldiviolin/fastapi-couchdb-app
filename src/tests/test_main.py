import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_item(item, item_id):
    response = client.get(f"/items/{item_id}/")
    assert response.status_code == 200
    assert response.json() == item


def test_get_item_with_inexistent_id(database):
    response = client.get("/items/999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "item_not_found"}


def test_get_items_without_any(database):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_items(items, item_dict):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == [item for item in items]


def test_add_item(database, item_dict, item_id):
    item_dict["id"] = item_id
    response = client.post("/items/", json=item_dict)
    assert response.status_code == 201
    assert response.json() == item_dict


def test_add_item_with_existing_id(item, item_dict, item_id):
    item_dict["id"] = item_id
    response = client.post("/items/", json=item_dict)
    assert response.status_code == 400
    assert response.json() == {"detail": "item_already_exists"}


def test_modify_item(item, item_dict, item_id):
    item_dict.update(
        {
            "name": "soap4",
            "description": "This is a soap 2.0",
            "price": 21.56,
        }
    )
    response = client.put(f"/items/{item_id}/", json=item_dict)
    assert response.status_code == 200
    item.update(item_dict)
    response_json = response.json()
    assert response_json == item


def test_modify_item_with_inexistent_id(database, item_dict, item_id):
    response = client.put(f"/items/{item_id}/", json=item_dict)
    assert response.status_code == 404
    assert response.json() == {"detail": "item_not_found"}


@pytest.mark.parametrize(
    "field_to_update,new_value",
    [
        ("name", "soap4"),
        ("description", "This is soap 2.0"),
        ("price", 21.56),
    ],
)
def test_modify_item_partially(field_to_update, new_value, item, item_dict, item_id):
    item_dict[field_to_update] = new_value
    response = client.patch(f"/items/{item_id}/", json=item_dict)
    assert response.status_code == 200
    item[field_to_update] = new_value
    response_json = response.json()
    assert response_json == item


def test_modify_item_partially_with_inexistent_id(database, item_dict, item_id):
    response = client.patch(f"/items/{item_id}/", json=item_dict)
    assert response.status_code == 404
    assert response.json() == {"detail": "item_not_found"}
