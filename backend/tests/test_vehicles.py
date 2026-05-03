import pytest

VEHICLE_PAYLOAD = {
    "name": "Test Benz",
    "sub": "Luxury Saloon · 2024",
    "tag": "luxury",
    "price": 60000,
    "image_url": "https://example.com/car.jpg",
}


def test_list_vehicles_empty(client):
    res = client.get("/api/v1/vehicles/")
    assert res.status_code == 200
    assert res.json() == []


def test_create_vehicle(client):
    res = client.post("/api/v1/vehicles/", json=VEHICLE_PAYLOAD)
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Test Benz"
    assert data["tag"] == "luxury"
    assert data["price"] == 60000
    assert "id" in data


def test_list_vehicles_returns_created(client):
    res = client.get("/api/v1/vehicles/")
    assert res.status_code == 200
    assert any(v["name"] == "Test Benz" for v in res.json())


def test_filter_by_tag(client):
    # Create a suv vehicle
    client.post("/api/v1/vehicles/", json={**VEHICLE_PAYLOAD, "name": "Defender", "tag": "suv"})
    res = client.get("/api/v1/vehicles/?tag=suv")
    assert res.status_code == 200
    assert all(v["tag"] == "suv" for v in res.json())


def test_filter_by_max_price(client):
    res = client.get("/api/v1/vehicles/?max_price=30000")
    assert res.status_code == 200
    assert all(v["price"] <= 30000 for v in res.json())


def test_get_vehicle_by_id(client):
    create_res = client.post("/api/v1/vehicles/", json=VEHICLE_PAYLOAD)
    vid = create_res.json()["id"]
    res = client.get(f"/api/v1/vehicles/{vid}")
    assert res.status_code == 200
    assert res.json()["id"] == vid


def test_get_vehicle_not_found(client):
    res = client.get("/api/v1/vehicles/99999")
    assert res.status_code == 404


def test_update_vehicle(client):
    create_res = client.post("/api/v1/vehicles/", json=VEHICLE_PAYLOAD)
    vid = create_res.json()["id"]
    res = client.patch(f"/api/v1/vehicles/{vid}", json={"price": 75000})
    assert res.status_code == 200
    assert res.json()["price"] == 75000


def test_delete_vehicle(client):
    create_res = client.post("/api/v1/vehicles/", json=VEHICLE_PAYLOAD)
    vid = create_res.json()["id"]
    res = client.delete(f"/api/v1/vehicles/{vid}")
    assert res.status_code == 204
    assert client.get(f"/api/v1/vehicles/{vid}").status_code == 404
