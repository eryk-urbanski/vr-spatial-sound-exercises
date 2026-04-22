from uuid import uuid4

from fastapi.testclient import TestClient

from tests.constants import SEEDED_SESSION_ID


def test_new_command_supersedes_previous_pending_command(client: TestClient) -> None:
    first_response = client.post(
        f"/api/dashboard/sessions/{SEEDED_SESSION_ID}/commands",
        json={"command_type": "pause_session", "payload": {"source": "therapist"}},
    )
    assert first_response.status_code == 201

    second_response = client.post(
        f"/api/dashboard/sessions/{SEEDED_SESSION_ID}/commands",
        json={"command_type": "end_session", "payload": {"reason": "manual_stop"}},
    )

    assert second_response.status_code == 201
    latest_response = client.get(f"/api/vr/sessions/{SEEDED_SESSION_ID}/commands/latest")
    latest_command = latest_response.json()["command"]

    assert latest_command["command_type"] == "end_session"
    assert latest_command["payload"] == {"reason": "manual_stop"}


def test_dashboard_command_roundtrip(client: TestClient) -> None:
    create_response = client.post(
        f"/api/dashboard/sessions/{SEEDED_SESSION_ID}/commands",
        json={"command_type": "end_session", "payload": {"reason": "therapist_request"}},
    )

    assert create_response.status_code == 201
    created_command = create_response.json()
    assert created_command["command_type"] == "end_session"
    assert created_command["status"] == "pending"

    poll_response = client.get(f"/api/vr/sessions/{SEEDED_SESSION_ID}/commands/latest")

    assert poll_response.status_code == 200
    body = poll_response.json()
    assert body["session_id"] == str(SEEDED_SESSION_ID)
    assert body["command"]["id"] == created_command["id"]
    assert body["command"]["payload"] == {"reason": "therapist_request"}


def test_polling_returns_null_when_no_command_exists(client: TestClient) -> None:
    response = client.get(f"/api/vr/sessions/{SEEDED_SESSION_ID}/commands/latest")

    assert response.status_code == 200
    assert response.json() == {"session_id": str(SEEDED_SESSION_ID), "command": None}


def test_vr_results_are_visible_to_dashboard(client: TestClient) -> None:
    create_response = client.post(
        f"/api/vr/sessions/{SEEDED_SESSION_ID}/results",
        json={"result_type": "exercise_summary", "payload": {"score": 8, "duration_seconds": 240}},
    )

    assert create_response.status_code == 201
    created_result = create_response.json()
    assert created_result["result_type"] == "exercise_summary"

    list_response = client.get(f"/api/dashboard/sessions/{SEEDED_SESSION_ID}/results")

    assert list_response.status_code == 200
    body = list_response.json()
    assert body["session"]["id"] == str(SEEDED_SESSION_ID)
    assert len(body["results"]) == 1
    assert body["results"][0]["id"] == created_result["id"]
    assert body["results"][0]["payload"]["score"] == 8


def test_invalid_payload_returns_422(client: TestClient) -> None:
    response = client.post(
        f"/api/vr/sessions/{SEEDED_SESSION_ID}/results",
        json={"result_type": "exercise_summary", "payload": "invalid"},
    )

    assert response.status_code == 422


def test_unknown_session_returns_404(client: TestClient) -> None:
    response = client.get(f"/api/dashboard/sessions/{uuid4()}/results")

    assert response.status_code == 404
