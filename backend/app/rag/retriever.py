from __future__ import annotations

from typing import Any

import chromadb

from backend.app.core.config import (
    RAG_COLLECTION_NAME,
    RAG_TOP_K,
    RAG_VECTORSTORE_PATH,
)
from backend.app.rag.embeddings import embed_query
from backend.app.rag.schemas import RagSearchResult


def get_collection(
    collection_name: str = RAG_COLLECTION_NAME,
):
    client = chromadb.PersistentClient(
        path=str(RAG_VECTORSTORE_PATH),
    )

    return client.get_collection(
        name=collection_name,
    )


def _parse_tags(value: Any) -> list[str]:
    if not value:
        return []

    if isinstance(value, list):
        return [str(item) for item in value]

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return []


def search(
    query: str,
    *,
    top_k: int = RAG_TOP_K,
    collection_name: str = RAG_COLLECTION_NAME,
) -> list[RagSearchResult]:
    collection = get_collection(collection_name)

    query_embedding = embed_query(query)

    response = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    ids = response.get("ids", [[]])[0]
    documents = response.get("documents", [[]])[0]
    metadatas = response.get("metadatas", [[]])[0]
    distances = response.get("distances", [[]])[0]

    results: list[RagSearchResult] = []

    for index, chunk_id in enumerate(ids):
        metadata = metadatas[index] or {}
        distance = distances[index] if distances else None

        score = None
        if distance is not None:
            score = 1.0 - float(distance)

        results.append(
            RagSearchResult(
                id=chunk_id,
                text=documents[index],
                title=metadata.get("title", ""),
                source_type=metadata.get("source_type", ""),
                source_file=metadata.get("source_file", ""),
                source_image=metadata.get("source_image"),
                page=metadata.get("page"),
                domain=metadata.get("domain", "general"),
                tags=_parse_tags(metadata.get("tags")),
                distance=distance,
                score=score,
                metadata=metadata,
            )
        )

    return results
