import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any


@dataclass
class IntentResult:
    intent: str
    confidence: float
    entities: dict[str, Any] = field(default_factory=dict)


class IntentService:
    """
    Routeur d'intention simple basé sur des règles.

    Cette première version n'utilise pas de LLM.
    L'objectif est d'avoir un comportement prévisible, testable et suffisant
    pour les scénarios principaux du MVP.
    """

    def detect_intent(self, message: str) -> IntentResult:
        text = self._normalize(message)
        entities = self._extract_entities(text)

        if self._contains_any(text, ["mot de passe", "password", "code secret", "pin"]):
            return IntentResult("out_of_scope", 0.95, entities)

        if self._contains_any(text, ["solde", "combien j'ai", "combien jai", "balance"]):
            return IntentResult("get_balance", 0.95, entities)

        if self._contains_any(text, ["transaction", "transactions", "operation", "operations", "mouvement", "mouvements"]):
            return IntentResult("get_transactions", 0.9, entities)

        if self._contains_any(text, ["virement", "transferer", "envoyer de l'argent", "envoyer argent"]):
            return IntentResult("prepare_transfer", 0.9, entities)

        if self._contains_any(text, ["bloquer ma carte", "bloque ma carte", "opposition", "carte perdue", "perdu ma carte", "vol de carte"]):
            return IntentResult("block_card", 0.95, entities)

        if self._contains_any(text, ["chequier", "carnet de cheque", "carnet de cheques", "commande de chequier"]):
            return IntentResult("request_checkbook", 0.9, entities)

        if self._contains_any(text, ["releve", "document", "attestation", "demande de document"]):
            return IntentResult("request_document", 0.85, entities)

        if self._contains_any(text, ["credit", "pret", "emprunt", "mensualite", "simulation"]):
            return IntentResult("simulate_credit", 0.9, entities)

        if self._contains_any(text, ["agence", "message a l'agence", "contacter mon agence"]):
            return IntentResult("contact_agency", 0.8, entities)

        if self._contains_any(text, ["support", "probleme de connexion", "bug", "erreur", "connexion"]):
            return IntentResult("contact_support", 0.85, entities)

        if self._contains_any(text, ["comment", "aide", "expliquer", "c'est quoi", "qu'est-ce que"]):
            return IntentResult("general_question", 0.7, entities)

        return IntentResult("general_question", 0.4, entities)

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = unicodedata.normalize("NFD", text)
        text = "".join(char for char in text if unicodedata.category(char) != "Mn")
        return text

    def _contains_any(self, text: str, keywords: list[str]) -> bool:
        return any(keyword in text for keyword in keywords)

    def _extract_entities(self, text: str) -> dict[str, Any]:
        entities: dict[str, Any] = {}

        amount = self._extract_amount(text)
        if amount is not None:
            entities["amount"] = amount

        duration_months = self._extract_duration_months(text)
        if duration_months is not None:
            entities["duration_months"] = duration_months

        card_last_digits = self._extract_card_last_digits(text)
        if card_last_digits is not None:
            entities["card_last_digits"] = card_last_digits

        return entities

    def _extract_amount(self, text: str) -> float | None:
        pattern = r"(\d+(?:[\s]\d{3})*(?:[,.]\d+)?)\s*(dt|tnd|dinars?|eur|€)?"
        matches = re.findall(pattern, text)

        if not matches:
            return None

        for raw_amount, _currency in matches:
            amount_str = raw_amount.replace(" ", "").replace(",", ".")
            try:
                amount = float(amount_str)
                if amount > 0:
                    return amount
            except ValueError:
                continue

        return None

    def _extract_duration_months(self, text: str) -> int | None:
        years_match = re.search(r"(\d+)\s*(ans|annees|annee)", text)
        if years_match:
            return int(years_match.group(1)) * 12

        months_match = re.search(r"(\d+)\s*(mois)", text)
        if months_match:
            return int(months_match.group(1))

        return None

    def _extract_card_last_digits(self, text: str) -> str | None:
        match = re.search(r"(?:termine par|finissant par|carte)\s*(\d{4})", text)
        if match:
            return match.group(1)

        return None
