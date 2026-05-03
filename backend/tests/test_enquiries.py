from datetime import date, timedelta

FUTURE_DATE = (date.today() + timedelta(days=60)).isoformat()

ENQUIRY_PAYLOAD = {
    "full_name": "Ravindi & Asanka",
    "phone": "+94771234567",
    "wedding_date": FUTURE_DATE,
    "vehicle_id": None,
    "pickup_time": "09:00",
    "return_time": "15:00",
    "notes": "Please add white roses.",
}


def test_create_enquiry(client):
    res = client.post("/api/v1/enquiries/", json=ENQUIRY_PAYLOAD)
    assert res.status_code == 201
    data = res.json()
    assert data["full_name"] == "Ravindi & Asanka"
    assert data["status"] == "pending"
    assert "id" in data


def test_list_enquiries(client):
    res = client.get("/api/v1/enquiries/")
    assert res.status_code == 200
    body = res.json()
    assert "total" in body
    assert "items" in body
    assert body["total"] >= 1


def test_get_enquiry_by_id(client):
    create_res = client.post("/api/v1/enquiries/", json=ENQUIRY_PAYLOAD)
    eid = create_res.json()["id"]
    res = client.get(f"/api/v1/enquiries/{eid}")
    assert res.status_code == 200
    assert res.json()["id"] == eid


def test_get_enquiry_not_found(client):
    res = client.get("/api/v1/enquiries/99999")
    assert res.status_code == 404


def test_update_status_to_confirmed(client):
    create_res = client.post("/api/v1/enquiries/", json=ENQUIRY_PAYLOAD)
    eid = create_res.json()["id"]
    res = client.patch(f"/api/v1/enquiries/{eid}/status", json={"status": "confirmed"})
    assert res.status_code == 200
    assert res.json()["status"] == "confirmed"


def test_update_status_to_cancelled(client):
    create_res = client.post("/api/v1/enquiries/", json=ENQUIRY_PAYLOAD)
    eid = create_res.json()["id"]
    res = client.patch(f"/api/v1/enquiries/{eid}/status", json={"status": "cancelled"})
    assert res.status_code == 200
    assert res.json()["status"] == "cancelled"


def test_invalid_status_rejected(client):
    create_res = client.post("/api/v1/enquiries/", json=ENQUIRY_PAYLOAD)
    eid = create_res.json()["id"]
    res = client.patch(f"/api/v1/enquiries/{eid}/status", json={"status": "approved"})
    assert res.status_code == 422


def test_past_wedding_date_rejected(client):
    past_payload = {**ENQUIRY_PAYLOAD, "wedding_date": "2020-01-01"}
    res = client.post("/api/v1/enquiries/", json=past_payload)
    assert res.status_code == 422


def test_invalid_time_format_rejected(client):
    bad_payload = {**ENQUIRY_PAYLOAD, "pickup_time": "9am"}
    res = client.post("/api/v1/enquiries/", json=bad_payload)
    assert res.status_code == 422


def test_filter_by_status(client):
    # Confirm one enquiry
    eid = client.post("/api/v1/enquiries/", json=ENQUIRY_PAYLOAD).json()["id"]
    client.patch(f"/api/v1/enquiries/{eid}/status", json={"status": "confirmed"})
    # Filter
    res = client.get("/api/v1/enquiries/?status=confirmed")
    assert res.status_code == 200
    items = res.json()["items"]
    assert all(e["status"] == "confirmed" for e in items)


def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
