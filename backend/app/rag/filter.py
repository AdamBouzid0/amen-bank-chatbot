from backend.app.rag.cleaner import normalize_for_matching
from backend.app.rag.schemas import SourceDocument


RELEVANT_KEYWORDS = {
    "amenet",
    "@mennet",
    "amen mobile",
    "banque digitale",
    "service digital",
    "services digitaux",
    "service en ligne",
    "services en ligne",
    "digitalisation",
    "experience client",
    "intelligence artificielle",
    "cybersecurite",
    "securite des donnees",
    "donnees personnelles",
    "protection des donnees",
    "compte",
    "solde",
    "mouvement",
    "transaction",
    "virement",
    "beneficiaire",
    "carte bancaire",
    "opposition carte",
    "deblocage carte",
    "carte prepayee",
    "chequier",
    "demande de document",
    "releve",
    "credit",
    "simulation de credit",
    "financement",
    "messagerie",
    "support",
    "reclamation",
    "tpe",
    "gestion du budget",
    "change",
    "sicav",
    "bourse",
    "inclusion financiere",
    "finance durable",
    "presentation resumee de la banque",
    "banque universelle",
}

NOISE_KEYWORDS = {
    "commissaires aux comptes",
    "etats financiers",
    "actionnaires",
    "capital social",
    "dividendes",
    "assemblee generale",
    "conseil de surveillance",
    "emprunt obligataire",
    "provisions collectives",
    "ratio de solvabilite",
    "tableau de mouvement des capitaux propres",
}


def keyword_hits(text: str, keywords: set[str]) -> list[str]:
    normalized_text = normalize_for_matching(text)

    return sorted(
        {
            keyword
            for keyword in keywords
            if normalize_for_matching(keyword) in normalized_text
        }
    )


def extract_tags(text: str, maximum: int = 10) -> list[str]:
    return keyword_hits(text, RELEVANT_KEYWORDS)[:maximum]


def infer_domain(text: str) -> str:
    normalized = normalize_for_matching(text)

    amenet_terms = {
        "amenet",
        "@mennet",
        "virement",
        "chequier",
        "opposition carte",
        "mouvement",
        "beneficiaire",
        "messagerie",
        "gestion du budget",
    }

    security_terms = {
        "cybersecurite",
        "securite",
        "donnees personnelles",
        "protection des donnees",
        "opposition",
    }

    digital_terms = {
        "amen mobile",
        "banque digitale",
        "digitalisation",
        "services digitaux",
        "service en ligne",
        "intelligence artificielle",
    }

    sustainability_terms = {
        "finance durable",
        "durabilite",
        "developpement durable",
        "inclusion financiere",
        "environnement",
    }

    if any(term in normalized for term in amenet_terms):
        return "amenet_help"

    if any(term in normalized for term in security_terms):
        return "security"

    if any(term in normalized for term in digital_terms):
        return "digital_services"

    if any(term in normalized for term in sustainability_terms):
        return "sustainability"

    return "institutional"


def filter_document(
    document: SourceDocument,
    minimum_length: int = 80,
) -> tuple[bool, str, int]:
    """
    Retourne :
    - décision de conservation ;
    - raison ;
    - score de pertinence.
    """
    text = document.text.strip()

    if len(text) < minimum_length:
        return False, "content_too_short", 0

    # L'analyse fonctionnelle des captures est considérée comme source principale.
    if document.source_type == "screenshot_analysis":
        return True, "amenet_analysis_source", 100

    relevant_hits = keyword_hits(
        f"{document.title}\n{document.section or ''}\n{text}",
        RELEVANT_KEYWORDS,
    )

    noise_hits = keyword_hits(text, NOISE_KEYWORDS)

    score = (len(relevant_hits) * 2) - len(noise_hits)

    if document.source_type == "pdf" and not relevant_hits:
        return False, "no_relevant_pdf_keyword", score

    if len(noise_hits) >= 3 and len(relevant_hits) <= 1:
        return False, "financial_or_legal_noise", score

    return True, "relevant_content", score
