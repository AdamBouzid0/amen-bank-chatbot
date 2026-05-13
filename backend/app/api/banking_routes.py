from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.app.services.mock_banking_service import MockBankingService

router = APIRouter(prefix="/banking", tags=["banking"])
service = MockBankingService()


class TransferPrepareRequest(BaseModel):
    client_id: str
    from_account_id: str
    amount: float = Field(gt=0)
    currency: str = "TND"
    reason: str
    to_account_id: str | None = None
    beneficiary_id: str | None = None
    execution_date: str | None = None


class BlockCardRequest(BaseModel):
    client_id: str
    card_id: str
    reason: str


class CheckbookRequest(BaseModel):
    client_id: str
    account_id: str
    checkbook_type: str = "25 chèques"


class DocumentRequest(BaseModel):
    client_id: str
    account_id: str
    document_type: str
    period: str | None = None


class CreditSimulationRequest(BaseModel):
    amount: float = Field(gt=0)
    duration_months: int = Field(gt=0)
    annual_rate: float = 0.08
    monthly_income: float | None = None


def handle_service_error(error: Exception) -> HTTPException:
    return HTTPException(status_code=400, detail=str(error))


@router.get("/clients")
def get_clients():
    return service.get_clients()


@router.get("/clients/{client_id}")
def get_client(client_id: str):
    try:
        return service.get_client(client_id)
    except ValueError as error:
        raise handle_service_error(error)


@router.get("/clients/{client_id}/accounts")
def get_accounts_by_client(client_id: str):
    try:
        return service.get_accounts_by_client(client_id)
    except ValueError as error:
        raise handle_service_error(error)


@router.get("/accounts/{account_id}/balance")
def get_balance(account_id: str):
    try:
        return service.get_balance(account_id)
    except ValueError as error:
        raise handle_service_error(error)


@router.get("/accounts/{account_id}/transactions")
def get_transactions(
    account_id: str,
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    direction: str | None = Query(default=None),
):
    try:
        return service.get_transactions(
            account_id=account_id,
            date_from=date_from,
            date_to=date_to,
            direction=direction,
        )
    except ValueError as error:
        raise handle_service_error(error)


@router.get("/clients/{client_id}/cards")
def get_cards_by_client(client_id: str):
    try:
        return service.get_cards_by_client(client_id)
    except ValueError as error:
        raise handle_service_error(error)


@router.get("/clients/{client_id}/beneficiaries")
def get_beneficiaries_by_client(client_id: str):
    try:
        return service.get_beneficiaries_by_client(client_id)
    except ValueError as error:
        raise handle_service_error(error)


@router.get("/clients/{client_id}/transfers")
def get_transfers_by_client(client_id: str):
    try:
        return service.get_transfers_by_client(client_id)
    except ValueError as error:
        raise handle_service_error(error)


@router.get("/clients/{client_id}/requests")
def get_requests_by_client(client_id: str):
    try:
        return service.get_requests_by_client(client_id)
    except ValueError as error:
        raise handle_service_error(error)


@router.post("/transfer/prepare")
def prepare_transfer(payload: TransferPrepareRequest):
    try:
        transfer = service.prepare_transfer(**payload.model_dump())
        return {
            "message": "Virement préparé dans l'environnement de simulation. Une confirmation utilisateur est nécessaire.",
            "requires_confirmation": True,
            "transfer": transfer,
        }
    except ValueError as error:
        raise handle_service_error(error)


@router.post("/card/block")
def block_card(payload: BlockCardRequest):
    try:
        result = service.block_card(**payload.model_dump())
        return {
            "message": "Opposition carte enregistrée dans l'environnement de simulation.",
            "requires_confirmation": True,
            "result": result,
        }
    except ValueError as error:
        raise handle_service_error(error)


@router.post("/checkbook/request")
def request_checkbook(payload: CheckbookRequest):
    try:
        request = service.request_checkbook(**payload.model_dump())
        return {
            "message": "Demande de chéquier enregistrée dans l'environnement de simulation.",
            "request": request,
        }
    except ValueError as error:
        raise handle_service_error(error)


@router.post("/document/request")
def request_document(payload: DocumentRequest):
    try:
        request = service.request_document(**payload.model_dump())
        return {
            "message": "Demande de document enregistrée dans l'environnement de simulation.",
            "request": request,
        }
    except ValueError as error:
        raise handle_service_error(error)


@router.post("/credit/simulate")
def simulate_credit(payload: CreditSimulationRequest):
    try:
        result = service.simulate_credit(**payload.model_dump())
        return {
            "message": "Simulation de crédit calculée.",
            "simulation": result,
        }
    except ValueError as error:
        raise handle_service_error(error)
