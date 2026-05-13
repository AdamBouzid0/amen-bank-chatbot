from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_clients():
    response = client.get("/banking/clients")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_client_accounts():
    response = client.get("/banking/clients/C001/accounts")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(account["client_id"] == "C001" for account in data)


def test_get_balance():
    response = client.get("/banking/accounts/ACC001/balance")

    assert response.status_code == 200
    data = response.json()
    assert data["account_id"] == "ACC001"
    assert data["currency"] == "TND"


def test_get_transactions_with_filters():
    response = client.get(
        "/banking/accounts/ACC001/transactions",
        params={
            "date_from": "2026-05-01",
            "date_to": "2026-05-12",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_cards_by_client():
    response = client.get("/banking/clients/C001/cards")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_beneficiaries_by_client():
    response = client.get("/banking/clients/C001/beneficiaries")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_credit_simulation():
    response = client.post(
        "/banking/credit/simulate",
        json={
            "amount": 20000,
            "duration_months": 60,
            "annual_rate": 0.08,
            "monthly_income": 1800,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Simulation de crédit calculée."
    assert data["simulation"]["monthly_payment"] > 0


def test_unknown_client_returns_error():
    response = client.get("/banking/clients/UNKNOWN")

    assert response.status_code == 400
