from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from backend.app.core.config import RAG_EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Charge le modèle d'embeddings une seule fois.
    """
    return SentenceTransformer(RAG_EMBEDDING_MODEL)


def _format_for_model(texts: list[str], mode: str) -> list[str]:
    """
    Les modèles E5 donnent de meilleurs résultats avec les préfixes :
    - query: pour les questions
    - passage: pour les documents
    """
    model_name = RAG_EMBEDDING_MODEL.lower()

    if "e5" not in model_name:
        return texts

    if mode == "query":
        return [f"query: {text}" for text in texts]

    return [f"passage: {text}" for text in texts]


def embed_texts(
    texts: list[str],
    *,
    mode: str = "passage",
) -> list[list[float]]:
    if not texts:
        return []

    model = get_embedding_model()

    formatted_texts = _format_for_model(
        texts,
        mode=mode,
    )

    embeddings = model.encode(
        formatted_texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.tolist()


def embed_query(query: str) -> list[float]:
    return embed_texts(
        [query],
        mode="query",
    )[0]
