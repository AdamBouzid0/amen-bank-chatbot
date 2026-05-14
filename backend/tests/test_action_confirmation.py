import shutil
from pathlib import Path

import pytest

from backend.app.core.config import DATA_MOCK_DIR
from backend.app.services.chat_service import ChatService
from backend.app.services.mock_banking_service import MockBankingService


@pytest.fixture()
def chat_service(tmp_path: Path) -> ChatService:
    test_data_dir = tmp_path / "mock"
    shutil.copytree(DATA_MOCK_DIR, test_data_dir)

    banking_service = MockBankingService(data_dir=test_data_dir)
    return ChatService(banking_service=banking_service)


def test_confirm_transfer_action(chat_service: ChatService):
    first_response = chat_service.handle_message(
        message="Je veux faire un virement de 500 DT",
        client_id="C001",
    )

    assert first_response["requires_confirmation"] is True
    assert first_response["pending_action"]["type"] == "transfer"

    second_response = chat_service.handle_message(
        message="oui",
        client_id="C001",
    )

    assert second_response["intent"] == "confirm_action"
    assert second_response["requires_confirmation"] is False
    assert second_response["data"]["status"] == "confirmed_simulation"


def test_cancel_pending_action(chat_service: ChatService):
    first_response = chat_service.handle_message(
        message="Je veux commander un chéquier",
        client_id="C001",
    )

    assert first_response["requires_confirmation"] is True

    second_response = chat_service.handle_message(
        message="non",
        client_id="C001",
    )

    assert second_response["intent"] == "cancel_action"
    assert second_response["requires_confirmation"] is False
    assert "annulée" in second_response["message"]


def test_confirm_block_card_action(chat_service: ChatService):
    first_response = chat_service.handle_message(
        message="Je veux bloquer ma carte qui termine par 4582",
        client_id="C001",
    )

    assert first_response["requires_confirmation"] is True
    assert first_response["pending_action"]["type"] == "block_card"

    second_response = chat_service.handle_message(
        message="oui",
        client_id="C001",
    )

    assert second_response["intent"] == "confirm_action"
    assert second_response["requires_confirmation"] is False
    assert second_response["data"]["card"]["status"] == "blocked"


def test_pending_action_requires_yes_or_no(chat_service: ChatService):
    first_response = chat_service.handle_message(
        message="Je veux demander un relevé",
        client_id="C001",
    )

    assert first_response["requires_confirmation"] is True

    second_response = chat_service.handle_message(
        message="Quel est mon solde ?",
        client_id="C001",
    )

    assert second_response["intent"] == "pending_confirmation"
    assert second_response["requires_confirmation"] is True
