import shutil
from pathlib import Path

import pytest

from backend.app.core.config import DATA_MOCK_DIR
from backend.app.services.mock_banking_service import MockBankingService


@pytest.fixture()
def mock_service(tmp_path: Path) -> MockBankingService:
    test_data_dir = tmp_path / "mock"
    shutil.copytree(DATA_MOCK_DIR, test_data_dir)
    return MockBankingService(data_dir=test_data_dir)


def test_get_clients(mock_service: MockBankingService):
    clients = mock_service.get_clients()

    assert len(clients) >= 2
    assert clients[0]["client_id"] == "C001"


def test_get_accounts_by_client(mock_service: MockBankingService):
    accounts = mock_service.get_accounts_by_client("C001")

    assert len(accounts) >= 3
    assert all(account["client_id"] == "C001" for account in accounts)


def test_get_balance(mock_service: MockBankingService):
    balance = mock_service.get_balance("ACC001")

    assert balance["account_id"] == "ACC001"
    assert balance["currency"] == "TND"
    assert "balance" in balance


def test_get_transactions_with_date_filter(mock_service: MockBankingService):
    transactions = mock_service.get_transactions(
        account_id="ACC001",
        date_from="2026-05-01",
        date_to="2026-05-12",
    )

    assert len(transactions) > 0
    assert all(transaction["account_id"] == "ACC001" for transaction in transactions)
    assert all("2026-05-01" <= transaction["date"] <= "2026-05-12" for transaction in transactions)


def test_get_transactions_with_direction_filter(mock_service: MockBankingService):
    transactions = mock_service.get_transactions(
        account_id="ACC001",
        direction="debit",
    )

    assert len(transactions) > 0
    assert all(transaction["direction"] == "debit" for transaction in transactions)


def test_prepare_transfer_to_beneficiary(mock_service: MockBankingService):
    transfer = mock_service.prepare_transfer(
        client_id="C001",
        from_account_id="ACC001",
        beneficiary_id="BEN001",
        amount=500.000,
        currency="TND",
        reason="Facture test",
    )

    assert transfer["client_id"] == "C001"
    assert transfer["from_account_id"] == "ACC001"
    assert transfer["beneficiary_id"] == "BEN001"
    assert transfer["amount"] == 500.000
    assert transfer["status"] == "pending_confirmation"


def test_block_card(mock_service: MockBankingService):
    result = mock_service.block_card(
        client_id="C001",
        card_id="CARD001",
        reason="Perte de carte",
    )

    assert result["card"]["status"] == "blocked"
    assert result["request"]["type"] == "card_opposition"


def test_simulate_credit(mock_service: MockBankingService):
    simulation = mock_service.simulate_credit(
        amount=20000,
        duration_months=60,
        annual_rate=0.08,
        monthly_income=1800,
    )

    assert simulation["amount"] == 20000
    assert simulation["duration_months"] == 60
    assert simulation["monthly_payment"] > 0
    assert "is_within_capacity" in simulation


def test_unknown_client_raises_error(mock_service: MockBankingService):
    with pytest.raises(ValueError):
        mock_service.get_client("UNKNOWN")
