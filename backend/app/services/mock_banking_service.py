import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from backend.app.core.config import DATA_MOCK_DIR


class MockBankingService:
    """
    Service bancaire simulé.

    Ce service lit et écrit dans des fichiers JSON locaux.
    Il ne manipule aucune donnée réelle et sert uniquement à reproduire
    un comportement bancaire pour le prototype.
    """

    def __init__(self, data_dir: Path = DATA_MOCK_DIR):
        self.data_dir = data_dir

    def _load_json(self, filename: str) -> list[dict[str, Any]]:
        path = self.data_dir / filename

        if not path.exists():
            return []

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_json(self, filename: str, data: list[dict[str, Any]]) -> None:
        path = self.data_dir / filename

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def _get_next_id(self, items: list[dict[str, Any]], prefix: str, id_field: str) -> str:
        if not items:
            return f"{prefix}001"

        numbers = []
        for item in items:
            raw_id = item.get(id_field, "")
            if raw_id.startswith(prefix):
                try:
                    numbers.append(int(raw_id.replace(prefix, "")))
                except ValueError:
                    pass

        next_number = max(numbers, default=0) + 1
        return f"{prefix}{next_number:03d}"

    def get_clients(self) -> list[dict[str, Any]]:
        return self._load_json("clients.json")

    def get_client(self, client_id: str) -> dict[str, Any]:
        clients = self.get_clients()

        for client in clients:
            if client["client_id"] == client_id:
                return client

        raise ValueError(f"Client introuvable: {client_id}")

    def get_accounts_by_client(self, client_id: str) -> list[dict[str, Any]]:
        self.get_client(client_id)
        accounts = self._load_json("accounts.json")
        return [account for account in accounts if account["client_id"] == client_id]

    def get_account(self, account_id: str) -> dict[str, Any]:
        accounts = self._load_json("accounts.json")

        for account in accounts:
            if account["account_id"] == account_id:
                return account

        raise ValueError(f"Compte introuvable: {account_id}")

    def get_balance(self, account_id: str) -> dict[str, Any]:
        account = self.get_account(account_id)

        return {
            "account_id": account["account_id"],
            "label": account["label"],
            "masked_account_number": account["masked_account_number"],
            "currency": account["currency"],
            "balance": account["balance"],
            "balance_date": account["balance_date"],
            "status": account["status"],
        }

    def get_transactions(
        self,
        account_id: str,
        date_from: str | None = None,
        date_to: str | None = None,
        direction: str | None = None,
    ) -> list[dict[str, Any]]:
        self.get_account(account_id)
        transactions = self._load_json("transactions.json")

        results = [
            transaction
            for transaction in transactions
            if transaction["account_id"] == account_id
        ]

        if direction:
            results = [
                transaction
                for transaction in results
                if transaction["direction"] == direction
            ]

        if date_from:
            results = [
                transaction
                for transaction in results
                if transaction["date"] >= date_from
            ]

        if date_to:
            results = [
                transaction
                for transaction in results
                if transaction["date"] <= date_to
            ]

        return sorted(results, key=lambda item: item["date"], reverse=True)

    def get_cards_by_client(self, client_id: str) -> list[dict[str, Any]]:
        self.get_client(client_id)
        cards = self._load_json("cards.json")
        return [card for card in cards if card["client_id"] == client_id]

    def get_card(self, card_id: str) -> dict[str, Any]:
        cards = self._load_json("cards.json")

        for card in cards:
            if card["card_id"] == card_id:
                return card

        raise ValueError(f"Carte introuvable: {card_id}")

    def get_beneficiaries_by_client(self, client_id: str) -> list[dict[str, Any]]:
        self.get_client(client_id)
        beneficiaries = self._load_json("beneficiaries.json")
        return [
            beneficiary
            for beneficiary in beneficiaries
            if beneficiary["client_id"] == client_id
        ]

    def get_transfers_by_client(self, client_id: str) -> list[dict[str, Any]]:
        self.get_client(client_id)
        transfers = self._load_json("transfers.json")
        return [transfer for transfer in transfers if transfer["client_id"] == client_id]

    def get_requests_by_client(self, client_id: str) -> list[dict[str, Any]]:
        self.get_client(client_id)
        requests = self._load_json("requests.json")
        return [request for request in requests if request["client_id"] == client_id]

    def prepare_transfer(
        self,
        client_id: str,
        from_account_id: str,
        amount: float,
        currency: str,
        reason: str,
        to_account_id: str | None = None,
        beneficiary_id: str | None = None,
        execution_date: str | None = None,
        status: str = "pending_confirmation",
    ) -> dict[str, Any]:
        self.get_client(client_id)
        from_account = self.get_account(from_account_id)

        if from_account["client_id"] != client_id:
            raise ValueError("Le compte à débiter n'appartient pas au client.")

        if amount <= 0:
            raise ValueError("Le montant du virement doit être positif.")

        if not to_account_id and not beneficiary_id:
            raise ValueError("Un compte destinataire ou un bénéficiaire est obligatoire.")

        if to_account_id:
            self.get_account(to_account_id)

        if beneficiary_id:
            beneficiaries = self.get_beneficiaries_by_client(client_id)
            beneficiary_ids = {beneficiary["beneficiary_id"] for beneficiary in beneficiaries}
            if beneficiary_id not in beneficiary_ids:
                raise ValueError("Bénéficiaire introuvable pour ce client.")

        transfers = self._load_json("transfers.json")
        transfer_id = self._get_next_id(transfers, "TR", "transfer_id")

        transfer = {
            "transfer_id": transfer_id,
            "client_id": client_id,
            "type": "account_to_account" if to_account_id else "beneficiary_transfer",
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
            "beneficiary_id": beneficiary_id,
            "amount": amount,
            "currency": currency,
            "reason": reason,
            "execution_date": execution_date or date.today().isoformat(),
            "status": status,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        transfers.append(transfer)
        self._save_json("transfers.json", transfers)

        return transfer

    def block_card(self, client_id: str, card_id: str, reason: str) -> dict[str, Any]:
        self.get_client(client_id)

        cards = self._load_json("cards.json")
        selected_card = None

        for card in cards:
            if card["card_id"] == card_id:
                selected_card = card
                break

        if selected_card is None:
            raise ValueError("Carte introuvable.")

        if selected_card["client_id"] != client_id:
            raise ValueError("Cette carte n'appartient pas au client.")

        selected_card["status"] = "blocked"
        self._save_json("cards.json", cards)

        request = self._create_request(
            client_id=client_id,
            request_type="card_opposition",
            details={
                "card_id": card_id,
                "masked_card_number": selected_card["masked_card_number"],
                "reason": reason,
            },
        )

        return {
            "card": selected_card,
            "request": request,
        }

    def request_checkbook(
        self,
        client_id: str,
        account_id: str,
        checkbook_type: str = "25 chèques",
    ) -> dict[str, Any]:
        self.get_client(client_id)
        account = self.get_account(account_id)

        if account["client_id"] != client_id:
            raise ValueError("Ce compte n'appartient pas au client.")

        return self._create_request(
            client_id=client_id,
            request_type="checkbook_request",
            details={
                "account_id": account_id,
                "masked_account_number": account["masked_account_number"],
                "checkbook_type": checkbook_type,
            },
        )

    def request_document(
        self,
        client_id: str,
        account_id: str,
        document_type: str,
        period: str | None = None,
    ) -> dict[str, Any]:
        self.get_client(client_id)
        account = self.get_account(account_id)

        if account["client_id"] != client_id:
            raise ValueError("Ce compte n'appartient pas au client.")

        return self._create_request(
            client_id=client_id,
            request_type="document_request",
            details={
                "account_id": account_id,
                "masked_account_number": account["masked_account_number"],
                "document_type": document_type,
                "period": period,
            },
        )

    def simulate_credit(
        self,
        amount: float,
        duration_months: int,
        annual_rate: float = 0.08,
        monthly_income: float | None = None,
    ) -> dict[str, Any]:
        if amount <= 0:
            raise ValueError("Le montant du crédit doit être positif.")

        if duration_months <= 0:
            raise ValueError("La durée doit être positive.")

        monthly_rate = annual_rate / 12

        if monthly_rate == 0:
            monthly_payment = amount / duration_months
        else:
            monthly_payment = (
                amount
                * monthly_rate
                / (1 - (1 + monthly_rate) ** (-duration_months))
            )

        result = {
            "amount": round(amount, 3),
            "duration_months": duration_months,
            "annual_rate": annual_rate,
            "monthly_payment": round(monthly_payment, 3),
            "total_repayment": round(monthly_payment * duration_months, 3),
            "currency": "TND",
        }

        if monthly_income is not None:
            max_recommended_payment = monthly_income * 0.4
            result["monthly_income"] = round(monthly_income, 3)
            result["max_recommended_payment"] = round(max_recommended_payment, 3)
            result["is_within_capacity"] = monthly_payment <= max_recommended_payment

        return result

    def _create_request(
        self,
        client_id: str,
        request_type: str,
        details: dict[str, Any],
    ) -> dict[str, Any]:
        requests = self._load_json("requests.json")
        request_id = self._get_next_id(requests, "REQ", "request_id")

        request = {
            "request_id": request_id,
            "client_id": client_id,
            "type": request_type,
            "status": "pending",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "details": details,
        }

        requests.append(request)
        self._save_json("requests.json", requests)

        return request
