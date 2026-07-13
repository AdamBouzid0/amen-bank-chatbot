from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.core.config import RAG_TOP_K
from backend.app.rag.rag_service import RagService


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)

rag_service = RagService()


class RagSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=RAG_TOP_K, ge=1, le=10)


class RagSearchResponse(BaseModel):
    query: str
    results: list[dict]


@router.get("/health")
def rag_health() -> dict:
    return {
        "status": "ok",
        "service": "rag",
    }


@router.post("/search", response_model=RagSearchResponse)
def search_documents(request: RagSearchRequest) -> RagSearchResponse:
    try:
        results = rag_service.search_documents(
            query=request.query,
            top_k=request.top_k,
        )

        return RagSearchResponse(
            query=request.query,
            results=[
                result.model_dump()
                for result in results
            ],
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la recherche RAG : {error}",
        ) from error
