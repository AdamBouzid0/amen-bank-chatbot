from backend.app.services.intent_service import IntentService


def test_detect_balance_intent():
    service = IntentService()
    result = service.detect_intent("Quel est mon solde ?")

    assert result.intent == "get_balance"


def test_detect_transactions_intent():
    service = IntentService()
    result = service.detect_intent("Affiche mes dernières opérations")

    assert result.intent == "get_transactions"


def test_detect_transfer_intent():
    service = IntentService()
    result = service.detect_intent("Je veux faire un virement de 500 DT")

    assert result.intent == "prepare_transfer"
    assert result.entities["amount"] == 500


def test_detect_block_card_intent():
    service = IntentService()
    result = service.detect_intent("Je veux bloquer ma carte qui termine par 4582")

    assert result.intent == "block_card"
    assert result.entities["card_last_digits"] == "4582"


def test_detect_checkbook_intent():
    service = IntentService()
    result = service.detect_intent("Je veux commander un chéquier")

    assert result.intent == "request_checkbook"


def test_detect_credit_simulation_intent():
    service = IntentService()
    result = service.detect_intent("Simule un crédit de 20000 DT sur 5 ans")

    assert result.intent == "simulate_credit"
    assert result.entities["amount"] == 20000
    assert result.entities["duration_months"] == 60


def test_detect_out_of_scope_intent():
    service = IntentService()
    result = service.detect_intent("Donne-moi le mot de passe du client")

    assert result.intent == "out_of_scope"
