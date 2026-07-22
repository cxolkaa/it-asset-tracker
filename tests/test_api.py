from datetime import date

from fastapi.testclient import TestClient

from app.database import Base, engine, SessionLocal
from app.main import app

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_asset():
    payload = {
        "name": "Dell Latitude 5540",
        "asset_type": "laptop",
        "serial_number": "SN-12345",
        "assigned_to": "Jan Kowalski",
        "department": "IT",
        "status": "active",
        "warranty_until": "2027-06-01",
    }
    create_resp = client.post("/assets", json=payload)
    assert create_resp.status_code == 201
    asset_id = create_resp.json()["id"]

    get_resp = client.get(f"/assets/{asset_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Dell Latitude 5540"


def test_duplicate_serial_rejected():
    payload = {"name": "Laptop A", "serial_number": "DUP-001"}
    assert client.post("/assets", json=payload).status_code == 201
    assert client.post("/assets", json=payload).status_code == 409


def test_expiring_warranties():
    client.post(
        "/assets",
        json={
            "name": "Monitor",
            "serial_number": "MON-1",
            "warranty_until": date.today().isoformat(),
        },
    )
    resp = client.get("/assets/warranties/expiring?days=30")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
