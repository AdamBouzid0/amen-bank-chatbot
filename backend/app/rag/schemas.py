from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


SourceType = Literal[
    "pdf",
    "markdown",
    "screenshot_analysis",
]


class SourceDocument(BaseModel):
    """
    Document ou section avant découpage en chunks.
    """

    id: str
    text: str = Field(min_length=1)
    title: str
    section: str | None = None

    source_type: SourceType
    source_file: str
    source_image: str | None = None
    page: int | None = None

    domain: str = "general"
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class TextChunk(BaseModel):
    """
    Passage final destiné à l'indexation dans la base vectorielle.
    """

    id: str
    parent_id: str
    chunk_index: int

    text: str = Field(min_length=1)
    title: str
    section: str | None = None

    source_type: SourceType
    source_file: str
    source_image: str | None = None
    page: int | None = None

    domain: str = "general"
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class RagSearchResult(BaseModel):
    """
    Résultat retourné par le retriever RAG.
    """

    id: str
    text: str
    title: str
    source_type: str
    source_file: str
    source_image: str | None = None
    page: int | None = None
    domain: str = "general"
    tags: list[str] = Field(default_factory=list)

    distance: float | None = None
    score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
