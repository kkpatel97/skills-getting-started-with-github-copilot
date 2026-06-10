import uuid
from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_participant():
    email = f"test-{uuid.uuid4().hex}@example.com"
    activity = "Chess Club"
    path = quote(activity, safe="")

    # Sign up
    signup = client.post(f"/activities/{path}/signup", params={"email": email})
    assert signup.status_code == 200

    # Participant should appear in GET
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

    # Unregister
    delete = client.delete(f"/activities/{path}/signup", params={"email": email})
    assert delete.status_code == 200

    activities_after = client.get("/activities").json()
    assert email not in activities_after[activity]["participants"]


def test_signup_nonexistent_activity():
    resp = client.post("/activities/NoSuchActivity/signup", params={"email": "a@b.com"})
    assert resp.status_code == 404


def test_unregister_nonexistent_participant():
    activity = "Chess Club"
    path = quote(activity, safe="")
    resp = client.delete(f"/activities/{path}/signup", params={"email": "not-present@example.com"})
    assert resp.status_code == 404
