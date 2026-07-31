import unicodedata
from typing import Any

from backend.app.rag.rag_service import RagService
from backend.app.services.intent_service import IntentService
from backend.app.services.mock_banking_service import MockBankingService


class ChatService:
    """
    Service principal du chatbot.

    Il reçoit un message utilisateur, détecte l'intention,
    appelle le service adapté et retourne une réponse structurée.

    Cette version gère aussi les actions en attente de confirmation.
    """

    def __init__(
        self,
        intent_service: IntentService | None = None,
        banking_service: MockBankingService | None = None,
        rag_service: RagService | None = None,
    ):
        self.intent_service = intent_service or IntentService()
        self.banking_service = banking_service or MockBankingService()
        self.rag_service = rag_service or RagService()
        self.pending_actions: dict[str, dict[str, Any]] = {}

    def handle_message(self, message: str, client_id: str = "C001") -> dict[str, Any]:
        normalized_message = self._normalize(message)

        if client_id in self.pending_actions:
            if self._is_confirmation(normalized_message):
                return self._confirm_pending_action(client_id)

            if self._is_cancellation(normalized_message):
                return self._cancel_pending_action(client_id)

            return {
                "message": (
                    "Une action est en attente de confirmation. "
                    "Répondez par 'oui' pour confirmer ou 'non' pour annuler."
                ),
                "intent": "pending_confirmation",
                "requires_confirmation": True,
                "pending_action": self.pending_actions[client_id],
                "data": {},
                "sources": [],
                "error": None,
            }

        intent_result = self.intent_service.detect_intent(message)
        intent = intent_result.intent
        entities = intent_result.entities

        if self._should_answer_with_rag(normalized_message, intent):
            return self._handle_general_question("general_question", message)

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

            return self._handle_general_question(intent, message)

        except ValueError as error:
            return {
                "message": str(error),
                "intent": intent,
                "requires_confirmation": False,
                "data": {},
                "sources": [],
                "error": str(error),
            }

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = unicodedata.normalize("NFD", text)
        return "".join(char for char in text if unicodedata.category(char) != "Mn")

    def _is_confirmation(self, text: str) -> bool:
        confirmations = {
            "oui",
            "yes",
            "ok",
            "d'accord",
            "daccord",
            "je confirme",
            "confirmer",
            "confirme",
            "valider",
            "valide",
        }
        return text in confirmations

    def _is_cancellation(self, text: str) -> bool:
        cancellations = {
            "non",
            "no",
            "annuler",
            "annule",
            "stop",
            "abandonner",
            "abandonne",
        }
        return text in cancellations

    def _should_answer_with_rag(self, normalized_message: str, intent: str) -> bool:
        action_intents = {
            "prepare_transfer",
            "block_card",
            "request_checkbook",
            "request_document",
        }

        if intent == "general_question":
            return True

        if intent in action_intents and self._is_information_question(normalized_message):
            return True

        return False

    def _is_information_question(self, normalized_message: str) -> bool:
        information_patterns = (
            "comment ",
            "comment faire",
            "comment demander",
            "comment commander",
            "comment bloquer",
            "comment debloquer",
            "comment consulter",
            "qu'est ce",
            "qu est ce",
            "c'est quoi",
            "c est quoi",
            "explique",
            "expliquez",
            "quelle est la procedure",
            "quelle procedure",
            "que dois je",
            "que faut il",
        )

        return (
            normalized_message.endswith("?")
            or any(
                normalized_message.startswith(pattern)
                for pattern in information_patterns
            )
        )

    def _store_pending_action(
        self,
        client_id: str,
        message: str,
        intent: str,
        pending_action: dict[str, Any],
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.pending_actions[client_id] = pending_action

        return {
            "message": message,
            "intent": intent,
            "requires_confirmation": True,
            "pending_action": pending_action,
            "data": data or {},
            "sources": [],
            "error": None,
        }

    def _confirm_pending_action(self, client_id: str) -> dict[str, Any]:
        pending_action = self.pending_actions.pop(client_id)

        try:
            action_type = pending_action["type"]

            if action_type == "transfer":
                result = self.banking_service.prepare_transfer(
                    client_id=pending_action["client_id"],
                    from_account_id=pending_action["from_account_id"],
                    amount=pending_action["amount"],
                    currency=pending_action["currency"],
                    reason=pending_action["reason"],
                    to_account_id=pending_action.get("to_account_id"),
                    beneficiary_id=pending_action.get("beneficiary_id"),
                    execution_date=pending_action.get("execution_date"),
                    status="confirmed_simulation",
                )

                return {
                    "message": "Le virement a été confirmé et enregistré dans l'environnement de simulation.",
                    "intent": "confirm_action",
                    "requires_confirmation": False,
                    "data": result,
                    "sources": [],
                    "error": None,
                }

            if action_type == "block_card":
                result = self.banking_service.block_card(
                    client_id=pending_action["client_id"],
                    card_id=pending_action["card_id"],
                    reason=pending_action["reason"],
                )

                return {
                    "message": "L'opposition sur carte a été confirmée et enregistrée dans l'environnement de simulation.",
                    "intent": "confirm_action",
                    "requires_confirmation": False,
                    "data": result,
                    "sources": [],
                    "error": None,
                }

            if action_type == "request_checkbook":
                result = self.banking_service.request_checkbook(
                    client_id=pending_action["client_id"],
                    account_id=pending_action["account_id"],
                    checkbook_type=pending_action["checkbook_type"],
                )

                return {
                    "message": "La demande de chéquier a été confirmée et enregistrée dans l'environnement de simulation.",
                    "intent": "confirm_action",
                    "requires_confirmation": False,
                    "data": result,
                    "sources": [],
                    "error": None,
                }

            if action_type == "request_document":
                result = self.banking_service.request_document(
                    client_id=pending_action["client_id"],
                    account_id=pending_action["account_id"],
                    document_type=pending_action["document_type"],
                    period=pending_action.get("period"),
                )

                return {
                    "message": "La demande de document a été confirmée et enregistrée dans l'environnement de simulation.",
                    "intent": "confirm_action",
                    "requires_confirmation": False,
                    "data": result,
                    "sources": [],
                    "error": None,
                }

            return {
                "message": "Action inconnue. La confirmation n'a pas pu être traitée.",
                "intent": "confirm_action",
                "requires_confirmation": False,
                "data": {},
                "sources": [],
                "error": "unknown_action",
            }

        except ValueError as error:
            return {
                "message": str(error),
                "intent": "confirm_action",
                "requires_confirmation": False,
                "data": {},
                "sources": [],
                "error": str(error),
            }

    def _cancel_pending_action(self, client_id: str) -> dict[str, Any]:
        self.pending_actions.pop(client_id)

        return {
            "message": "L'action en attente a été annulée.",
            "intent": "cancel_action",
            "requires_confirmation": False,
            "data": {},
            "sources": [],
            "error": None,
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

        return self._store_pending_action(
            client_id=client_id,
            intent=intent,
            pending_action=pending_action,
            data={
                "account": account,
                "beneficiary": beneficiary,
            },
            message=(
                f"Je peux préparer un virement de {amount:.3f} TND depuis "
                f"{account['label']} vers {target}. Confirmez-vous cette opération ?"
            ),
        )

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

        return self._store_pending_action(
            client_id=client_id,
            intent=intent,
            pending_action=pending_action,
            data={
                "card": selected_card,
            },
            message=(
                f"Vous souhaitez faire opposition sur la carte "
                f"{selected_card['masked_card_number']}. Confirmez-vous cette opération ?"
            ),
        )

    def _handle_request_checkbook(self, client_id: str, intent: str, entities: dict[str, Any]) -> dict[str, Any]:
        account = self._get_default_account(client_id)

        return self._store_pending_action(
            client_id=client_id,
            intent=intent,
            pending_action={
                "type": "request_checkbook",
                "client_id": client_id,
                "account_id": account["account_id"],
                "checkbook_type": "25 chèques",
            },
            data={
                "account": account,
            },
            message=(
                f"Je peux préparer une demande de chéquier pour le compte "
                f"{account['masked_account_number']}. Confirmez-vous la demande ?"
            ),
        )

    def _handle_request_document(self, client_id: str, intent: str, entities: dict[str, Any]) -> dict[str, Any]:
        account = self._get_default_account(client_id)

        return self._store_pending_action(
            client_id=client_id,
            intent=intent,
            pending_action={
                "type": "request_document",
                "client_id": client_id,
                "account_id": account["account_id"],
                "document_type": "Relevé de compte",
                "period": "Mois courant",
            },
            data={
                "account": account,
            },
            message=(
                f"Je peux préparer une demande de relevé de compte pour "
                f"{account['masked_account_number']}. Confirmez-vous la demande ?"
            ),
        )

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

    def _handle_general_question(self, intent: str, original_message: str) -> dict[str, Any]:
        try:
            results = self.rag_service.search_documents(
                query=original_message,
                top_k=3,
            )
        except Exception as error:
            return self._fallback_general_question(
                intent=intent,
                error=str(error),
            )

        relevant_results = [
            result
            for result in results
            if result.score is None or result.score >= 0.45
        ]

        if not relevant_results:
            return self._fallback_general_question(intent=intent)

        return {
            "message": self._build_rag_message(relevant_results, original_message),
            "intent": intent,
            "requires_confirmation": False,
            "data": {
                "rag_results_count": len(relevant_results),
            },
            "sources": [
                self._format_rag_source(result)
                for result in relevant_results
            ],
            "error": None,
        }

    def _fallback_general_question(
        self,
        intent: str,
        error: str | None = None,
    ) -> dict[str, Any]:
        message = (
            "Je peux vous aider sur les fonctionnalités AMENet comme la consultation du solde, "
            "les mouvements, les virements, l'opposition carte, les demandes de documents, "
            "la simulation de crédit et la messagerie."
        )

        if error:
            message += (
                "\n\nLe module documentaire RAG est temporairement indisponible. "
                "Vérifiez que l'index a bien été construit avec scripts/build_rag_index.py."
            )

        return {
            "message": message,
            "intent": intent,
            "requires_confirmation": False,
            "data": {},
            "sources": [],
            "error": error,
        }

    def _build_rag_message(self, results: list[Any], original_message: str) -> str:
        if not results:
            return (
                "Je n'ai pas trouvé d'information suffisamment pertinente "
                "dans la base documentaire du prototype."
            )

        main_result = results[0]
        answer = self._build_natural_rag_answer(
            main_result=main_result,
            original_message=original_message,
        )

        complementary_points = self._build_complementary_points(results[1:3])

        if complementary_points:
            answer += "\n\nÀ retenir également :\n" + complementary_points

        return answer

    def _build_natural_rag_answer(self, main_result: Any, original_message: str) -> str:
        title = (main_result.title or "").lower()
        text = main_result.text or ""

        if "opposition" in title and "carte" in title:
            return (
                "Pour faire opposition à une carte, le chatbot doit d'abord identifier "
                "la carte concernée. Pour des raisons de sécurité, il n'affiche que les "
                "cartes masquées, par exemple avec les derniers chiffres visibles. "
                "Une fois la carte choisie, il demande une confirmation explicite avant "
                "d'enregistrer la demande d'opposition dans l'environnement de simulation."
            )

        if "chéquier" in title or "chequier" in title:
            return (
                "Pour commander un chéquier, le chatbot identifie le compte concerné, "
                "prépare une demande de chéquier et demande une confirmation explicite "
                "avant d'enregistrer la demande dans l'environnement de simulation."
            )

        if "document" in title or "relevé" in title or "releve" in title:
            return (
                "Pour demander un document bancaire, le chatbot identifie le compte concerné "
                "et le type de document demandé, par exemple un relevé de compte. "
                "La demande est ensuite soumise à confirmation avant d'être enregistrée "
                "dans l'environnement de simulation."
            )

        if "virement" in title:
            return (
                "Pour préparer un virement, le chatbot doit identifier le compte source, "
                "le montant, la devise et le bénéficiaire. Comme il s'agit d'une action "
                "sensible, le virement n'est jamais enregistré directement : une confirmation "
                "explicite de l'utilisateur est obligatoire."
            )

        if "confirmation" in title or "actions sensibles" in title:
            return (
                "Les opérations sensibles, comme les virements, l'opposition sur carte, "
                "les demandes de documents ou les commandes de chéquier, doivent toujours "
                "être confirmées explicitement par l'utilisateur avant d'être enregistrées "
                "dans l'environnement de simulation."
            )

        if "service" in title or "périmètre" in title or "perimetre" in title:
            return (
                "Le prototype couvre plusieurs services AMENet : consultation du solde, "
                "affichage des mouvements, préparation de virements, opposition sur carte, "
                "demande de chéquier, demande de document, simulation de crédit et messagerie. "
                "Les opérations restent simulées et ne sont pas connectées à un système bancaire réel."
            )

        dialogue_answer = self._answer_from_dialogue_example(text)

        if dialogue_answer:
            return dialogue_answer

        excerpt = self._clean_rag_excerpt(text, max_length=650)

        return (
            "D'après la base documentaire du prototype, voici l'information pertinente :\n\n"
            f"{excerpt}"
        )

    def _answer_from_dialogue_example(self, text: str) -> str | None:
        if "Utilisateur :" not in text or "Chatbot :" not in text:
            return None

        assistant_parts = []
        fragments = text.split("Chatbot :")[1:]

        for fragment in fragments:
            assistant_text = fragment.split("Utilisateur :", 1)[0].strip()
            assistant_text = self._truncate_text(assistant_text, max_length=220)

            if assistant_text:
                assistant_parts.append(assistant_text)

        if not assistant_parts:
            return None

        lines = [
            "Dans le prototype, le parcours prévu est le suivant :"
        ]

        for part in assistant_parts[:3]:
            lines.append(f"- {part}")

        return "\n".join(lines)

    def _build_complementary_points(self, results: list[Any]) -> str:
        points = []

        for result in results:
            title = result.title or "Source complémentaire"
            excerpt = self._clean_rag_excerpt(
                result.text or "",
                max_length=220,
            )
            points.append(f"- **{title}** : {excerpt}")

        return "\n".join(points)

    def _clean_rag_excerpt(self, text: str, max_length: int = 700) -> str:
        cleaned = text.strip()

        cleaned = cleaned.replace("Utilisateur :", "")
        cleaned = cleaned.replace("Chatbot :", "")

        lines = [
            line.strip()
            for line in cleaned.splitlines()
            if line.strip()
        ]

        cleaned = " ".join(lines)
        cleaned = self._truncate_text(cleaned, max_length=max_length)

        return cleaned

    def _format_rag_source(self, result: Any) -> dict[str, Any]:
        return {
            "title": result.title,
            "source_type": result.source_type,
            "source_file": result.source_file,
            "source_image": result.source_image,
            "page": result.page,
            "domain": result.domain,
            "tags": result.tags,
            "score": result.score,
        }

    def _truncate_text(self, text: str, max_length: int = 900) -> str:
        clean_text = text.strip()

        if len(clean_text) <= max_length:
            return clean_text

        truncated = clean_text[:max_length].rsplit(" ", 1)[0]
        return f"{truncated}..."

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
