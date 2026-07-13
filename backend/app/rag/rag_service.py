from __future__ import annotations

from backend.app.core.config import RAG_TOP_K
from backend.app.rag.retriever import search
from backend.app.rag.schemas import RagSearchResult


class RagService:
    def search_documents(
        self,
        query: str,
        *,
        top_k: int = RAG_TOP_K,
    ) -> list[RagSearchResult]:
        return search(
            query,
            top_k=top_k,
        )

    def build_context(
        self,
        query: str,
        *,
        top_k: int = RAG_TOP_K,
    ) -> str:
        results = self.search_documents(
            query,
            top_k=top_k,
        )

        context_parts: list[str] = []

        for index, result in enumerate(results, start=1):
            source = result.source_file

            if result.page is not None:
                source = f"{source}, page {result.page}"

            context_parts.append(
                f"[Source {index}] {result.title}\n"
                f"Origine : {source}\n"
                f"{result.text}"
            )

        return "\n\n---\n\n".join(context_parts)
