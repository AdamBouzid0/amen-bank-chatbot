from typing import Any

from backend.app.services.intent_service import IntentService
from backend.app.services.mock_banking_service import MockBankingService


class ChatService:
    """
    Service principal du chatbot.

    Il reçoit un message utilisateur, détecte l'intention,
    appelle le service adapté et retourne une réponse structurée.
    """

    def __init__(self):
        self.intent_service = IntentService()
        self.banking_service = MockBankingService()

    def handle_message(self, message: str, client_id: str = "C001") -> dict[str, Any]:
        intent_result = self.intent_service.detect_intent(message)
        intent = intent_result.intent
        entities = intent_result.entities

        try:
            if intent == "get_balance":
                return self._handle_get_balance(client_id, intent, entities)

            if intent == "get_transactions":
                return self._handle_get_transactions(client_id, intent, entities)

            if intent == "prepare_transfer":
                return self._handle_prepare_transfer(client_id, intent, entities)

            if intent == "block_card":
                return self._handle_block_card(client_id, intent, entities)

            if intent == "request_checkbook":
                return self._handle_request_checkbook(client_id, intent, entities)

            if intent == "request_document":
                return self._handle_request_document(client_id, intent, entities)

            if intent == "simulate_credit":
                return self._handle_simulate_credit(intent, entities)

            if intent == "contact_agency":
                return self._handle_contact_agency(intent)

            if intent == "contact_support":
                return self._handle_contact_support(intent, message)

            if intent == "out_of_scope":
                return self._handle_out_of_scope(intent)

            return self._handle_general_question(intent)

        except ValueError as error:
            return {
                "message": str(error),
                "intent": intent,
                "requires_confirmation": False,
                "data": {},
                "sources": [],
                "error": str(error),
            }

    def _get_default_account(self, client_id: str) -> dict[str, Any]:
        accounts = self.banking_service.get_accounts_by_client(client_id)

        if not accounts:
            raise ValueError("Aucun compte disponible pour ce client fictif.")

        return accounts[0]

    def _handle_get_balance(self, client_id: str, intent: str, entities: dict[str, Any]) -> dict[str, Any]:
        account = self._get_default_account(client_id)
        balance = self.banking_service.get_balance(account["account_id"])

        return {
            "message": (
                f"Le solde du {balance['label']} "
                f"({balance['masked_account_number']}) est de "
                f"{balance['balance']:.3f} {balance['currency']} "
                f"au {balance['balance_date']}."
            ),
            "intent": intent,
            "requires_confirmation": False,
            "data": balance,
            "sources": [],
            "error": None,
        }

    def _handle_get_transactions(self, client_id: str, intent: str, entities: dict[str, Any]) -> dict[str, Any]:
        account = self._get_default_account(client_id)
        transactions = self.banking_service.get_transactions(account["account_id"])

        displayed_transactions = transactions[:5]
        total_debits = sum(abs(tx["amount"]) for tx in transactions if tx["direction"] == "debit")
        total_credits = sum(tx["amount"] for tx in transactions if tx["direction"] == "credit")

        lines = [
            f"- {tx['date']} : {tx['label']} ({tx['amount']:.3f} TND)"
            for tx in displayed_transactions
        ]

        message = (
            f"Voici les dernières opérations du {account['label']} "
            f"({account['masked_account_number']}) :\n"
            + "\n".join(lines)
            + f"\n\nTotal crédits : {total_credits:.3f} TND. "
            + f"Total débits : {total_debits:.3f} TND."
        )

        return {
            "message": message,
            "intent": intent,
            "requires_confirmation": False,
            "data": {
                "account": account,
                "transactions": displayed_transactions,
                "total_debits": round(total_debits, 3),
                "total_credits": round(total_credits, 3),
            },
            "sources": [],
            "error": None,
        }

    def _handle_prepare_transfer(self, client_id: str, intent: str, entities: dict[str, Any]) -> dict[str, Any]:
        amount = entities.get("amount")

        if amount is None:
            return {
                "message": "Pour préparer un virement, veuillez préciser le montant.",
                "intent": intent,
                "requires_confirmation": False,
                "data": {},
                "sources": [],
                "error": None,
            }

        account = self._get_default_account(client_id)
        beneficiaries = self.banking_service.get_beneficiaries_by_client(client_id)
        beneficiary = beneficiaries[0] if beneficiaries else None

        pending_action = {
            "type": "transfer",
            "client_id": client_id,
            "from_account_id": account["account_id"],
            "amount": amount,
            "currency": "TND",
            "beneficiary_id": beneficiary["beneficiary_id"] if beneficiary else None,
            "reason": "Virement préparé depuis le chatbot",
        }

        target = beneficiary["name"] if beneficiary else "un bénéficiaire à préciser"

        return {
            "message": (
                f"Je peux préparer un virement de {amount:.3f} TND depuis "
                f"{account['label']} vers {target}. Confirmez-vous cette opération ?"
            ),
            "intent": intent,
            "requires_confirmation": True,
            "pending_action": pending_action,
            "data": {
                "account": account,
                "beneficiary": beneficiary,
            },
            "sources": [],
            "error": None,
        }

    def _handle_block_card(self, client_id: str, intent: str, entities: dict[str, Any]) -> dict[str, Any]:
        cards = self.banking_service.get_cards_by_client(client_id)
        if not cards:
            raise ValueError("Aucune carte disponible pour ce client fictif.")

        selected_card = cards[0]
        last_digits = entities.get("card_last_digits")

        if last_digits:
            for card in cards:
                if card["masked_card_number"].endswith(last_digits):
                    selected_card = card
                    break

        pending_action = {
            "type": "block_card",
            "client_id": client_id,
            "card_id": selected_card["card_id"],
            "reason": "Demande d'opposition depuis le chatbot",
        }

        return {
            "message": (
                f"Vous souhaitez faire opposition sur la carte "
                f"{selected_card['masked_card_number']}. Confirmez-vous cette opération ?"
            ),
            "intent": intent,
            "requires_confirmation": True,
            "pending_action": pending_action,
            "data": {
                "card": selected_card,
            },
            "sources": [],
            "error": None,
        }

    def _handle_request_checkbook(self, client_id: str, intent: str, entities: dict[str, Any]) -> dict[str, Any]:
        account = self._get_default_account(client_id)

        return {
            "message": (
                f"Je peux préparer une demande de chéquier pour le compte "
                f"{account['masked_account_number']}. Confirmez-vous la demande ?"
            ),
            "intent": intent,
            "requires_confirmation": True,
            "pending_action": {
                "type": "request_checkbook",
                "client_id": client_id,
                "account_id": account["account_id"],
                "checkbook_type": "25 chèques",
            },
            "data": {
                "account": account,
            },
            "sources": [],
            "error": None,
        }

    def _handle_request_document(self, client_id: str, intent: str, entities: dict[str, Any]) -> dict[str, Any]:
        account = self._get_default_account(client_id)

        return {
            "message": (
                f"Je peux préparer une demande de relevé de compte pour "
                f"{account['masked_account_number']}. Confirmez-vous la demande ?"
            ),
            "intent": intent,
            "requires_confirmation": True,
            "pending_action": {
                "type": "request_document",
                "client_id": client_id,
                "account_id": account["account_id"],
                "document_type": "Relevé de compte",
                "period": "Mois courant",
            },
            "data": {
                "account": account,
            },
            "sources": [],
            "error": None,
        }

    def _handle_simulate_credit(self, intent: str, entities: dict[str, Any]) -> dict[str, Any]:
        amount = entities.get("amount", 20000.0)
        duration_months = entities.get("duration_months", 60)

        simulation = self.banking_service.simulate_credit(
            amount=amount,
            duration_months=duration_months,
            annual_rate=0.08,
            monthly_income=1800,
        )

        return {
            "message": (
                f"Pour un crédit de {simulation['amount']:.3f} TND sur "
                f"{simulation['duration_months']} mois, la mensualité estimée est de "
                f"{simulation['monthly_payment']:.3f} TND. "
                f"Le remboursement total estimé est de {simulation['total_repayment']:.3f} TND."
            ),
            "intent": intent,
            "requires_confirmation": False,
            "data": simulation,
            "sources": [],
            "error": None,
        }

    def _handle_contact_agency(self, intent: str) -> dict[str, Any]:
        return {
            "message": (
                "Voici un message proposé pour votre agence :\n\n"
                "Bonjour, je souhaite obtenir une assistance concernant mon espace AMENet. "
                "Merci de bien vouloir me contacter pour m'accompagner dans ma demande."
            ),
            "intent": intent,
            "requires_confirmation": False,
            "data": {},
            "sources": [],
            "error": None,
        }

    def _handle_contact_support(self, intent: str, original_message: str) -> dict[str, Any]:
        return {
            "message": (
                "Voici un message proposé pour le support :\n\n"
                f"Bonjour, je rencontre le problème suivant sur AMENet : {original_message}. "
                "Merci de bien vouloir m'assister."
            ),
            "intent": intent,
            "requires_confirmation": False,
            "data": {},
            "sources": [],
            "error": None,
        }

    def _handle_general_question(self, intent: str) -> dict[str, Any]:
        return {
            "message": (
                "Je peux vous aider sur les fonctionnalités AMENet comme la consultation du solde, "
                "les mouvements, les virements, l'opposition carte, les demandes de documents, "
                "la simulation de crédit et la messagerie. "
                "Le module documentaire RAG sera ajouté dans une prochaine version."
            ),
            "intent": intent,
            "requires_confirmation": False,
            "data": {},
            "sources": [],
            "error": None,
        }

    def _handle_out_of_scope(self, intent: str) -> dict[str, Any]:
        return {
            "message": (
                "Je ne peux pas traiter cette demande pour des raisons de sécurité. "
                "Je ne peux pas fournir de mot de passe, de code secret ou d'information sensible."
            ),
            "intent": intent,
            "requires_confirmation": False,
            "data": {},
            "sources": [],
            "error": None,
        }
