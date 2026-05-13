from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


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
    assert "transactions" in str(data["data"]).lower() or "operations" in data["message"].lower()


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
