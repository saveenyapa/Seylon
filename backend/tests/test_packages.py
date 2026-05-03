PACKAGE_PAYLOAD = {
    "name": "The Vow",
    "slug": "the-vow-test",
    "hours": 2,
    "description": "Ceremony to reception.",
    "price": 30000,
    "is_featured": False,
    "features": [
        {"text": "Tuxedoed chauffeur",   "included": True,  "sort_order": 1},
        {"text": "Backup vehicle",        "included": False, "sort_order": 2},
    ],
}


def test_list_packages_empty(client):
    res = client.get("/api/v1/packages/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_create_package_with_features(client):
    res = client.post("/api/v1/packages/", json=PACKAGE_PAYLOAD)
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "The Vow"
    assert data["slug"] == "the-vow-test"
    assert len(data["features"]) == 2
    assert data["features"][0]["text"] == "Tuxedoed chauffeur"
    assert data["features"][0]["included"] is True
    assert data["features"][1]["included"] is False


def test_duplicate_slug_rejected(client):
    res = client.post("/api/v1/packages/", json=PACKAGE_PAYLOAD)
    assert res.status_code == 409


def test_get_package_by_id(client):
    create_res = client.post(
        "/api/v1/packages/", json={**PACKAGE_PAYLOAD, "slug": "unique-slug-1"}
    )
    pid = create_res.json()["id"]
    res = client.get(f"/api/v1/packages/{pid}")
    assert res.status_code == 200
    assert res.json()["id"] == pid


def test_get_package_not_found(client):
    res = client.get("/api/v1/packages/99999")
    assert res.status_code == 404


def test_featured_package_flag(client):
    res = client.post(
        "/api/v1/packages/",
        json={**PACKAGE_PAYLOAD, "slug": "featured-test", "is_featured": True},
    )
    assert res.status_code == 201
    assert res.json()["is_featured"] is True
