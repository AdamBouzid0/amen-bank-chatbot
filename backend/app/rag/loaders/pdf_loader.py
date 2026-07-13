from __future__ import annotations

import hashlib
from pathlib import Path

import pymupdf

from backend.app.rag.cleaner import clean_text
from backend.app.rag.filter import extract_tags, infer_domain
from backend.app.rag.schemas import SourceDocument


def _relative_path(path: Path, project_root: Path | None) -> str:
    if project_root is None:
        return path.as_posix()

    try:
        return path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _detect_page_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        candidate = line.strip()

        if not candidate:
            continue

        if candidate.isdigit():
            continue

        if 4 <= len(candidate) <= 150:
            return candidate

    return fallback


def load_pdf(
    path: str | Path,
    *,
    project_root: str | Path | None = None,
) -> list[SourceDocument]:
    pdf_path = Path(path)
    root_path = Path(project_root) if project_root else None
    source_file = _relative_path(pdf_path, root_path)

    documents: list[SourceDocument] = []

    pdf = pymupdf.open(pdf_path)

    try:
        pdf_metadata = pdf.metadata or {}
        pdf_title = pdf_metadata.get("title") or pdf_path.stem

        for page_index, page in enumerate(pdf):
            raw_text = page.get_text("text", sort=True)
            text = clean_text(raw_text)

            if len(text) < 40:
                continue

            page_number = page_index + 1
            page_title = _detect_page_title(text, pdf_title)

            fingerprint = (
                f"{source_file}|{page_number}|{text[:300]}"
            )

            document_id = hashlib.sha1(
                fingerprint.encode("utf-8")
            ).hexdigest()[:16]

            combined_text = f"{page_title}\n{text}"

            documents.append(
                SourceDocument(
                    id=f"pdf_{document_id}",
                    text=text,
                    title=page_title,
                    section=f"Page {page_number}",
                    source_type="pdf",
                    source_file=source_file,
                    page=page_number,
                    domain=infer_domain(combined_text),
                    tags=extract_tags(combined_text),
                    metadata={
                        "pdf_title": pdf_title,
                        "total_pages": len(pdf),
                    },
                )
            )
    finally:
        pdf.close()

    return documents


def save_documents_as_markdown(
    documents: list[SourceDocument],
    output_path: str | Path,
) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []

    for document in documents:
        page_label = (
            f"Page {document.page}"
            if document.page is not None
            else document.section or "Section"
        )

        lines.extend(
            [
                f"## {page_label} — {document.title}",
                "",
                document.text,
                "",
            ]
        )

    destination.write_text(
        "\n".join(lines).strip() + "\n",
        encoding="utf-8",
    )
