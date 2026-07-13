from __future__ import annotations

import hashlib
import re

from backend.app.rag.schemas import SourceDocument, TextChunk


DEFAULT_MAX_CHARS = 1800
DEFAULT_OVERLAP_CHARS = 250


def _recursive_split(
    text: str,
    max_chars: int,
    separators: list[str],
) -> list[str]:
    text = text.strip()

    if not text:
        return []

    if len(text) <= max_chars:
        return [text]

    if not separators:
        return [
            text[index:index + max_chars].strip()
            for index in range(0, len(text), max_chars)
            if text[index:index + max_chars].strip()
        ]

    separator = separators[0]
    parts = text.split(separator)

    if len(parts) == 1:
        return _recursive_split(
            text,
            max_chars,
            separators[1:],
        )

    results: list[str] = []
    current = ""

    for part in parts:
        part = part.strip()

        if not part:
            continue

        candidate = (
            f"{current}{separator}{part}".strip()
            if current
            else part
        )

        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            results.append(current.strip())
            current = ""

        if len(part) > max_chars:
            results.extend(
                _recursive_split(
                    part,
                    max_chars,
                    separators[1:],
                )
            )
        else:
            current = part

    if current:
        results.append(current.strip())

    return results


def split_text(
    text: str,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> list[str]:
    separators = [
        "\n\n",
        "\n",
        ". ",
        "; ",
        ", ",
        " ",
    ]

    return _recursive_split(
        text,
        max_chars,
        separators,
    )


def _overlap_prefix(
    previous_text: str,
    overlap_chars: int,
) -> str:
    if overlap_chars <= 0:
        return ""

    tail = previous_text[-overlap_chars:]

    whitespace_match = re.search(r"\s", tail)

    if whitespace_match:
        tail = tail[whitespace_match.start():]

    return tail.strip()


def chunk_document(
    document: SourceDocument,
    *,
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap_chars: int = DEFAULT_OVERLAP_CHARS,
) -> list[TextChunk]:
    pieces = split_text(
        document.text,
        max_chars=max_chars,
    )

    chunks: list[TextChunk] = []

    for index, piece in enumerate(pieces):
        final_text = piece

        if index > 0 and overlap_chars > 0:
            prefix = _overlap_prefix(
                pieces[index - 1],
                overlap_chars,
            )

            if prefix:
                final_text = f"{prefix}\n\n{piece}"

        fingerprint = (
            f"{document.id}|{index}|{final_text}"
        )

        chunk_hash = hashlib.sha1(
            fingerprint.encode("utf-8")
        ).hexdigest()[:16]

        chunks.append(
            TextChunk(
                id=f"chunk_{chunk_hash}",
                parent_id=document.id,
                chunk_index=index,
                text=final_text,
                title=document.title,
                section=document.section,
                source_type=document.source_type,
                source_file=document.source_file,
                source_image=document.source_image,
                page=document.page,
                domain=document.domain,
                tags=document.tags,
                metadata=document.metadata.copy(),
            )
        )

    return chunks


def chunk_documents(
    documents: list[SourceDocument],
    *,
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap_chars: int = DEFAULT_OVERLAP_CHARS,
) -> list[TextChunk]:
    chunks: list[TextChunk] = []

    for document in documents:
        chunks.extend(
            chunk_document(
                document,
                max_chars=max_chars,
                overlap_chars=overlap_chars,
            )
        )

    return chunks
