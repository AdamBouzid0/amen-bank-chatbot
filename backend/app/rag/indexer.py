from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import chromadb

from backend.app.core.config import (
    RAG_CHUNKS_PATH,
    RAG_EMBEDDING_BATCH_SIZE,
    RAG_COLLECTION_NAME,
    RAG_VECTORSTORE_PATH,
)
from backend.app.rag.embeddings import embed_texts
from backend.app.rag.schemas import TextChunk


def load_chunks(path: str | Path = RAG_CHUNKS_PATH) -> list[TextChunk]:
    chunks_path = Path(path)

    if not chunks_path.exists():
        raise FileNotFoundError(
            f"Fichier chunks introuvable : {chunks_path}"
        )

    chunks: list[TextChunk] = []

    with chunks_path.open("r", encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                chunks.append(TextChunk.model_validate_json(line))
            except Exception as error:
                raise ValueError(
                    f"Erreur de lecture JSONL ligne {line_number} "
                    f"dans {chunks_path}: {error}"
                ) from error

    return chunks


def _metadata_to_chroma(chunk: TextChunk) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "parent_id": chunk.parent_id,
        "chunk_index": chunk.chunk_index,
        "title": chunk.title,
        "source_type": chunk.source_type,
        "source_file": chunk.source_file,
        "domain": chunk.domain,
        "tags": ", ".join(chunk.tags),
    }

    if chunk.section:
        metadata["section"] = chunk.section

    if chunk.source_image:
        metadata["source_image"] = chunk.source_image

    if chunk.page is not None:
        metadata["page"] = chunk.page

    if chunk.metadata:
        metadata["extra_metadata"] = json.dumps(
            chunk.metadata,
            ensure_ascii=False,
        )

    return metadata


def get_chroma_client() -> chromadb.PersistentClient:
    RAG_VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)

    return chromadb.PersistentClient(
        path=str(RAG_VECTORSTORE_PATH),
    )


def reset_collection(
    client: chromadb.PersistentClient,
    collection_name: str,
) -> None:
    existing_names = [
        collection.name
        for collection in client.list_collections()
    ]

    if collection_name in existing_names:
        client.delete_collection(collection_name)


def build_index(
    *,
    chunks_path: str | Path = RAG_CHUNKS_PATH,
    collection_name: str = RAG_COLLECTION_NAME,
    recreate: bool = True,
) -> int:
    chunks = load_chunks(chunks_path)

    if not chunks:
        raise ValueError(
            "Aucun chunk trouvé. Lance d'abord "
            "scripts/ingest_rag_sources.py."
        )

    client = get_chroma_client()

    if recreate:
        reset_collection(
            client,
            collection_name,
        )

    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={
            "description": "Corpus RAG AMEN BANK chatbot prototype",
            "hnsw:space": "cosine",
        },
    )

    total = 0

    for start in range(0, len(chunks), RAG_EMBEDDING_BATCH_SIZE):
        batch = chunks[start:start + RAG_EMBEDDING_BATCH_SIZE]

        texts = [chunk.text for chunk in batch]
        embeddings = embed_texts(
            texts,
            mode="passage",
        )

        collection.add(
            ids=[chunk.id for chunk in batch],
            documents=texts,
            metadatas=[
                _metadata_to_chroma(chunk)
                for chunk in batch
            ],
            embeddings=embeddings,
        )

        total += len(batch)

        print(
            f"Indexation : {total}/{len(chunks)} chunks"
        )

    return total
