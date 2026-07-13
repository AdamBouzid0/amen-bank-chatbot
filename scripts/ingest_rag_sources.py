from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from backend.app.rag.chunker import chunk_documents
from backend.app.rag.filter import filter_document
from backend.app.rag.loaders.markdown_loader import load_markdown
from backend.app.rag.loaders.pdf_loader import (
    load_pdf,
    save_documents_as_markdown,
)


ANALYSIS_FILE = PROJECT_ROOT / "docs" / "analyse_amenet.md"
SCREENSHOT_DIRECTORY = (
    PROJECT_ROOT / "data" / "raw" / "amenet_observations"
)
PDF_DIRECTORY = (
    PROJECT_ROOT / "data" / "raw" / "documents_publics"
)

EXTRACTED_PDF_DIRECTORY = (
    PROJECT_ROOT / "data" / "extracted" / "pdf"
)

PROCESSED_DIRECTORY = PROJECT_ROOT / "data" / "processed"

DOCUMENTS_OUTPUT = PROCESSED_DIRECTORY / "documents.jsonl"
CHUNKS_OUTPUT = PROCESSED_DIRECTORY / "chunks.jsonl"
REJECTED_OUTPUT = PROCESSED_DIRECTORY / "rejected_chunks.jsonl"


def model_to_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump()

    if hasattr(value, "dict"):
        return value.dict()

    if isinstance(value, dict):
        return value

    raise TypeError(
        f"Type non sérialisable : {type(value).__name__}"
    )


def write_jsonl(
    path: Path,
    values: list[Any],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as output:
        for value in values:
            output.write(
                json.dumps(
                    model_to_dict(value),
                    ensure_ascii=False,
                )
                + "\n"
            )


def main() -> None:
    documents = []

    if ANALYSIS_FILE.exists():
        amenet_documents = load_markdown(
            ANALYSIS_FILE,
            source_type="screenshot_analysis",
            screenshot_directory=SCREENSHOT_DIRECTORY,
            default_domain="amenet_help",
            project_root=PROJECT_ROOT,
        )

        documents.extend(amenet_documents)

        print(
            f"Analyse AMENet : {len(amenet_documents)} sections chargées."
        )
    else:
        print(
            f"Attention : fichier absent : {ANALYSIS_FILE}"
        )

    PDF_DIRECTORY.mkdir(parents=True, exist_ok=True)
    EXTRACTED_PDF_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    pdf_files = sorted(PDF_DIRECTORY.glob("*.pdf"))

    for pdf_path in pdf_files:
        pdf_documents = load_pdf(
            pdf_path,
            project_root=PROJECT_ROOT,
        )

        documents.extend(pdf_documents)

        markdown_output = (
            EXTRACTED_PDF_DIRECTORY
            / f"{pdf_path.stem}.md"
        )

        save_documents_as_markdown(
            pdf_documents,
            markdown_output,
        )

        print(
            f"{pdf_path.name} : "
            f"{len(pdf_documents)} pages textuelles extraites."
        )

    if not pdf_files:
        print(
            "Aucun PDF trouvé dans "
            "data/raw/documents_publics/."
        )

    accepted_documents = []
    rejected_documents = []

    for document in documents:
        keep, reason, score = filter_document(document)

        record = model_to_dict(document)
        record["filter_reason"] = reason
        record["relevance_score"] = score

        if keep:
            document.metadata["relevance_score"] = score
            accepted_documents.append(document)
        else:
            rejected_documents.append(record)

    chunks = chunk_documents(
        accepted_documents,
        max_chars=1800,
        overlap_chars=250,
    )

    write_jsonl(
        DOCUMENTS_OUTPUT,
        accepted_documents,
    )

    write_jsonl(
        CHUNKS_OUTPUT,
        chunks,
    )

    write_jsonl(
        REJECTED_OUTPUT,
        rejected_documents,
    )

    print()
    print("Ingestion terminée")
    print("-------------------")
    print(f"Documents chargés : {len(documents)}")
    print(f"Documents retenus : {len(accepted_documents)}")
    print(f"Documents rejetés : {len(rejected_documents)}")
    print(f"Chunks créés      : {len(chunks)}")
    print()
    print(f"Documents : {DOCUMENTS_OUTPUT}")
    print(f"Chunks    : {CHUNKS_OUTPUT}")
    print(f"Rejets    : {REJECTED_OUTPUT}")


if __name__ == "__main__":
    main()
