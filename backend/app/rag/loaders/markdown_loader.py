from __future__ import annotations

import hashlib
import re
from difflib import SequenceMatcher
from pathlib import Path

from backend.app.rag.cleaner import clean_text, normalize_for_matching
from backend.app.rag.filter import extract_tags, infer_domain
from backend.app.rag.schemas import SourceDocument, SourceType


HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

STOP_WORDS = {
    "de",
    "du",
    "des",
    "la",
    "le",
    "les",
    "un",
    "une",
    "a",
    "au",
    "aux",
    "et",
    "sur",
    "pour",
    "par",
}


def _relative_path(path: Path, project_root: Path | None) -> str:
    if project_root is None:
        return path.as_posix()

    try:
        return path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _meaningful_tokens(text: str) -> set[str]:
    return {
        token
        for token in normalize_for_matching(text).split()
        if token not in STOP_WORDS and not token.isdigit()
    }


def find_matching_screenshot(
    title: str,
    screenshot_directory: Path | None,
    project_root: Path | None = None,
) -> str | None:
    if screenshot_directory is None or not screenshot_directory.exists():
        return None

    title_normalized = normalize_for_matching(title)
    title_tokens = _meaningful_tokens(title)

    best_path: Path | None = None
    best_score = 0.0

    for screenshot in screenshot_directory.glob("*.png"):
        filename_normalized = normalize_for_matching(screenshot.stem)
        filename_tokens = _meaningful_tokens(screenshot.stem)

        similarity = SequenceMatcher(
            None,
            title_normalized,
            filename_normalized,
        ).ratio()

        union = title_tokens | filename_tokens
        overlap = (
            len(title_tokens & filename_tokens) / len(union)
            if union
            else 0.0
        )

        score = (0.65 * overlap) + (0.35 * similarity)

        if score > best_score:
            best_score = score
            best_path = screenshot

    if best_path is None or best_score < 0.35:
        return None

    return _relative_path(best_path, project_root)


def load_markdown(
    path: str | Path,
    *,
    source_type: SourceType = "markdown",
    screenshot_directory: str | Path | None = None,
    default_domain: str | None = None,
    project_root: str | Path | None = None,
) -> list[SourceDocument]:
    markdown_path = Path(path)
    root_path = Path(project_root) if project_root else None

    screenshots_path = (
        Path(screenshot_directory)
        if screenshot_directory
        else None
    )

    raw_text = markdown_path.read_text(encoding="utf-8")

    documents: list[SourceDocument] = []
    heading_stack: dict[int, str] = {}

    current_title = markdown_path.stem
    current_section = markdown_path.stem
    current_lines: list[str] = []

    source_file = _relative_path(markdown_path, root_path)

    def flush_section() -> None:
        nonlocal current_lines

        text = clean_text("\n".join(current_lines))
        current_lines = []

        if len(text) < 40:
            return

        fingerprint = (
            f"{source_file}|{current_section}|{text[:300]}"
        )

        document_id = hashlib.sha1(
            fingerprint.encode("utf-8")
        ).hexdigest()[:16]

        combined_text = f"{current_title}\n{current_section}\n{text}"

        source_image = find_matching_screenshot(
            current_title,
            screenshots_path,
            root_path,
        )

        documents.append(
            SourceDocument(
                id=f"md_{document_id}",
                text=text,
                title=current_title,
                section=current_section,
                source_type=source_type,
                source_file=source_file,
                source_image=source_image,
                domain=default_domain or infer_domain(combined_text),
                tags=extract_tags(combined_text),
            )
        )

    for line in raw_text.splitlines():
        heading_match = HEADING_PATTERN.match(line)

        if not heading_match:
            current_lines.append(line)
            continue

        flush_section()

        level = len(heading_match.group(1))
        heading_title = heading_match.group(2).strip()

        heading_stack = {
            existing_level: existing_title
            for existing_level, existing_title in heading_stack.items()
            if existing_level < level
        }

        heading_stack[level] = heading_title

        current_title = heading_title
        current_section = " > ".join(
            heading_stack[key]
            for key in sorted(heading_stack)
        )

    flush_section()

    return documents
