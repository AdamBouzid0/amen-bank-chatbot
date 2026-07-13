import re
import unicodedata


def normalize_for_matching(text: str) -> str:
    """
    Normalise une chaîne pour les comparaisons, filtres et recherches.
    """
    normalized = unicodedata.normalize("NFKD", text)
    normalized = "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )

    normalized = normalized.lower()
    normalized = re.sub(r"[^a-z0-9@]+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()


def clean_text(text: str) -> str:
    """
    Nettoyage léger conservant les paragraphes et les listes.
    """
    if not text:
        return ""

    text = text.replace("\u00a0", " ")
    text = text.replace("\u202f", " ")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Corrige les mots coupés en fin de ligne dans certains PDF.
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)

    cleaned_lines: list[str] = []
    previous_line = None

    for raw_line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", raw_line).strip()

        if not line:
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            continue

        # Évite certaines répétitions consécutives de titres ou pieds de page.
        if line == previous_line:
            continue

        cleaned_lines.append(line)
        previous_line = line

    cleaned = "\n".join(cleaned_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()
