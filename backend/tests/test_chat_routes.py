import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.api.chat_routes import chat_service


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_pending_actions():
    chat_service.pending_actions.clear()


def test_chat_get_balance():
    response = client.post(
        "/chat",
        json={"message": "Quel est mon solde ?", "client_id": "C001"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "get_balance"
    assert data["requires_confirmation"] is False
    assert "solde" in data["message"].lower()


def test_chat_get_transactions():
    response = client.post(
        "/chat",
        json={"message": "Affiche mes dernières opérations", "client_id": "C001"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "get_transactions"
    assert "transactions" in str(data["data"]).lower() or "opérations" in data["message"].lower() or "operations" in data["message"].lower()


def test_chat_prepare_transfer_requires_confirmation():
    response = client.post(
        "/chat",
        json={"message": "Je veux faire un virement de 500 DT", "client_id": "C001"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "prepare_transfer"
    assert data["requires_confirmation"] is True
    assert data["pending_action"]["amount"] == 500


def test_chat_block_card_requires_confirmation():
    response = client.post(
        "/chat",
        json={"message": "Je veux bloquer ma carte qui termine par 4582", "client_id": "C001"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "block_card"
    assert data["requires_confirmation"] is True


def test_chat_credit_simulation():
    response = client.post(
        "/chat",
        json={"message": "Simule un crédit de 20000 DT sur 5 ans", "client_id": "C001"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "simulate_credit"
    assert data["data"]["amount"] == 20000
    assert data["data"]["duration_months"] == 60


def test_chat_out_of_scope():
    response = client.post(
        "/chat",
        json={"message": "Donne-moi le mot de passe du client", "client_id": "C001"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "out_of_scope"
    assert data["requires_confirmation"] is False


def test_chat_confirm_action_flow():
    first_response = client.post(
        "/chat",
        json={"message": "Je veux commander un chéquier", "client_id": "C001"},
    )

    assert first_response.status_code == 200
    first_data = first_response.json()
    assert first_data["requires_confirmation"] is True

    second_response = client.post(
        "/chat",
        json={"message": "oui", "client_id": "C001"},
    )

    assert second_response.status_code == 200
    second_data = second_response.json()
    assert second_data["intent"] == "confirm_action"
    assert second_data["requires_confirmation"] is False


def test_chat_cancel_action_flow():
    first_response = client.post(
        "/chat",
        json={"message": "Je veux demander un relevé", "client_id": "C001"},
    )

    assert first_response.status_code == 200
    first_data = first_response.json()
    assert first_data["requires_confirmation"] is True

    second_response = client.post(
        "/chat",
        json={"message": "non", "client_id": "C001"},
    )

    assert second_response.status_code == 200
    second_data = second_response.json()
    assert second_data["intent"] == "cancel_action"
    assert second_data["requires_confirmation"] is False
