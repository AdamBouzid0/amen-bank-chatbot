from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])
chat_service = ChatService()


class ChatRequest(BaseModel):
    message: str
    client_id: str = "C001"


@router.post("")
def chat(payload: ChatRequest):
    return chat_service.handle_message(
        message=payload.message,
        client_id=payload.client_id,
    )
