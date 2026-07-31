from __future__ import annotations

import re
import unicodedata
from typing import Any

import requests

from backend.app.core.config import (
    OLLAMA_BASE_URL,
    OLLAMA_ENABLED,
    OLLAMA_MAX_CONTEXT_CHARS,
    OLLAMA_MODEL,
    OLLAMA_TIMEOUT_SECONDS,
)


class OllamaAnswerer:
    """
    Génère une réponse naturelle à partir des chunks RAG récupérés.

    Principe :
    - le retriever sélectionne les sources ;
    - le backend construit un brouillon sûr à partir du contexte ;
    - Ollama reformule ce brouillon sans ajouter de nouvelles informations ;
    - si Ollama hallucine ou devient risqué, on retourne None pour laisser ChatService utiliser le fallback.
    """

    def generate_answer(self, query: str, results: list[Any]) -> str | None:
        if not OLLAMA_ENABLED:
            return None

        context = self._build_context(results)
        safe_draft = self._build_safe_draft(query=query, results=results)

        if not context and not safe_draft:
            return None

        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": OLLAMA_MODEL,
                    "messages": [
                        {
                            "role": "system",
                            "content": self._build_system_prompt(),
                        },
                        {
                            "role": "user",
                            "content": self._build_user_prompt(
                                query=query,
                                safe_draft=safe_draft,
                                context=context,
                            ),
                        },
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.0,
                        "top_p": 0.7,
                        "num_predict": 260,
                    },
                },
                timeout=(3, OLLAMA_TIMEOUT_SECONDS),
            )

            response.raise_for_status()
            payload = response.json()

            answer = payload.get("message", {}).get("content", "").strip()
            answer = self._postprocess_answer(answer)

            if not answer:
                return None

            if not self._is_safe_grounded_answer(query=query, answer=answer):
                return None

            return answer

        except requests.exceptions.RequestException:
            return None

    def _build_system_prompt(self) -> str:
        return """
Tu es un assistant de reformulation pour un prototype académique AMENet.

Ton rôle :
- Tu ne réalises aucune opération bancaire.
- Tu ne démarres aucun parcours d'action.
- Tu reformules uniquement le brouillon sûr fourni par le backend.
- Le contexte documentaire sert seulement à vérifier le brouillon.

Règles obligatoires :
- N'ajoute aucune information qui n'est pas présente dans le brouillon ou le contexte.
- N'utilise pas tes connaissances générales sur les banques.
- Ne mentionne aucun délai.
- Ne mentionne pas de service client, agence, notification ou procédure externe si ce n'est pas explicitement dans le brouillon.
- Ne demande jamais à l'utilisateur de fournir un numéro de carte, des chiffres de carte, un mot de passe, un PIN, un code secret ou une donnée confidentielle.
- Ne dis jamais : "donnez-moi", "veuillez me fournir", "pour continuer", "avant de continuer", "je vais", "nous allons procéder".
- Pour une question informationnelle, explique la procédure de manière générale.
- Ne parle pas comme si une opération était déjà en cours.
- Ne recopie pas le dialogue brut "Utilisateur / Chatbot".
- Ne liste pas les sources : elles sont affichées séparément par l'interface.
- Réponds toujours en français.
- Style attendu : clair, professionnel, naturel, court.
""".strip()

    def _build_user_prompt(self, query: str, safe_draft: str, context: str) -> str:
        return f"""
Question utilisateur :
{query}

Type de demande :
Question informationnelle. Il faut expliquer la procédure, pas lancer une opération.

Brouillon sûr à reformuler :
{safe_draft}

Contexte documentaire récupéré par le RAG :
{context}

Tâche :
Reformule le brouillon sûr pour produire une réponse naturelle et claire.
Ne change pas le sens.
N'ajoute aucun fait nouveau.
Ne demande aucune information à l'utilisateur.
Ne mentionne pas les scores de similarité.
Réponds en un court paragraphe ou en 3 étapes maximum.
""".strip()

    def _build_safe_draft(self, query: str, results: list[Any]) -> str:
        normalized_query = self._normalize(query)

        if "opposition" in normalized_query and "carte" in normalized_query:
            return (
                "Pour faire opposition à une carte dans le prototype, le chatbot identifie "
                "d'abord la carte concernée sans afficher de numéro complet. Il affiche "
                "uniquement des cartes masquées, par exemple avec les derniers chiffres visibles. "
                "Une fois la carte choisie, il demande une confirmation explicite avant "
                "d'enregistrer la demande d'opposition dans l'environnement de simulation. "
                "Aucune opération bancaire réelle n'est exécutée."
            )

        if "chequier" in normalized_query:
            return (
                "Pour commander un chéquier dans le prototype, le chatbot identifie le compte "
                "concerné, prépare une demande de chéquier et demande une confirmation explicite "
                "avant d'enregistrer la demande dans l'environnement de simulation."
            )

        if "releve" in normalized_query or "document" in normalized_query:
            return (
                "Pour demander un document bancaire dans le prototype, le chatbot identifie "
                "le compte concerné et le type de document demandé. La demande est ensuite "
                "soumise à confirmation avant d'être enregistrée dans l'environnement de simulation."
            )

        if "virement" in normalized_query:
            return (
                "Pour préparer un virement dans le prototype, le chatbot identifie le compte source, "
                "le montant et le bénéficiaire. Comme il s'agit d'une action sensible, une confirmation "
                "explicite est nécessaire avant l'enregistrement dans l'environnement de simulation."
            )

        if "confirmation" in normalized_query or "actions sensibles" in normalized_query:
            return (
                "Dans le prototype, les actions sensibles comme les virements, l'opposition sur carte, "
                "les demandes de documents ou les commandes de chéquier nécessitent une confirmation "
                "explicite. Le chatbot reformule l'action avant de l'enregistrer dans l'environnement "
                "de simulation."
            )

        if "services" in normalized_query or "disponibles" in normalized_query:
            return (
                "Le prototype couvre plusieurs services AMENet : consultation du solde, affichage "
                "des mouvements, préparation de virements, opposition sur carte, demande de chéquier, "
                "demande de document, simulation de crédit et messagerie. Toutes les opérations restent simulées."
            )

        if results:
            main_text = getattr(results[0], "text", "") or ""
            return self._clean_text(main_text, max_length=700)

        return ""

    def _build_context(self, results: list[Any]) -> str:
        blocks = []
        current_size = 0

        for index, result in enumerate(results, start=1):
            title = getattr(result, "title", "Source sans titre")
            text = getattr(result, "text", "") or ""
            source_file = getattr(result, "source_file", None)
            source_image = getattr(result, "source_image", None)
            page = getattr(result, "page", None)

            sanitized_text = self._sanitize_context_text(
                title=title,
                text=text,
            )

            block = (
                f"[Source {index}]\n"
                f"Titre: {title}\n"
                f"Fichier: {source_file}\n"
                f"Capture: {source_image}\n"
                f"Page: {page}\n"
                f"Faits autorisés:\n{sanitized_text}\n"
            )

            if current_size + len(block) > OLLAMA_MAX_CONTEXT_CHARS:
                break

            blocks.append(block)
            current_size += len(block)

        return "\n---\n".join(blocks)

    def _sanitize_context_text(self, title: str, text: str) -> str:
        normalized_title = self._normalize(title)

        if "opposition" in normalized_title and "carte" in normalized_title:
            return (
                "L'opposition sur carte est une action sensible dans le prototype. "
                "Le chatbot identifie la carte concernée sans afficher de numéro complet. "
                "Il affiche uniquement des cartes masquées. "
                "Il demande une confirmation explicite avant d'enregistrer la demande. "
                "La demande est enregistrée uniquement dans l'environnement de simulation."
            )

        if "confirmation" in normalized_title or "operations sensibles" in normalized_title:
            return (
                "Les actions sensibles ne doivent pas être exécutées directement. "
                "Le chatbot doit reformuler l'action demandée et demander une confirmation explicite."
            )

        if "separation entre information et action" in normalized_title:
            return (
                "Le chatbot distingue les questions informationnelles des demandes d'action. "
                "Une question comme 'Comment faire opposition à ma carte ?' est une demande d'information. "
                "Une demande comme 'Bloque ma carte' déclenche un parcours d'action avec confirmation."
            )

        return self._clean_text(text, max_length=1000)

    def _is_safe_grounded_answer(self, query: str, answer: str) -> bool:
        normalized_query = self._normalize(query)
        normalized_answer = self._normalize(answer)

        forbidden_always = (
            "mot de passe",
            "code secret",
            "code pin",
            " pin ",
            "numero complet de carte",
            "numero de carte complet",
            "identifiant confidentiel",
            "contactez directement",
            "service client",
            "jours ouvrables",
            "notification",
            "donnez moi",
            "veuillez me donner",
            "veuillez me fournir",
            "pour continuer",
            "avant de continuer",
            "je vais",
            "nous allons proceder",
            "nous allons suivre",
            "n'hesitez pas a me fournir",
            "fournir plus de details",
        )

        if any(pattern in normalized_answer for pattern in forbidden_always):
            return False

        # Rejette les faux numéros de carte ou exemples qui ressemblent à un numéro complet.
        if re.search(r"\b\d{4}[\s-]\d{4}[\s-]\d{4}[\s-]\d{4}\b", answer):
            return False

        if "opposition" in normalized_query and "carte" in normalized_query:
            required_patterns = (
                "confirmation",
                "simulation",
            )

            if not all(pattern in normalized_answer for pattern in required_patterns):
                return False

        return True

    def _clean_text(self, text: str, max_length: int = 700) -> str:
        cleaned = text.strip()
        cleaned = cleaned.replace("Utilisateur :", "")
        cleaned = cleaned.replace("Chatbot :", "")

        lines = [
            line.strip()
            for line in cleaned.splitlines()
            if line.strip()
        ]

        cleaned = " ".join(lines)

        if len(cleaned) <= max_length:
            return cleaned

        return cleaned[:max_length].rsplit(" ", 1)[0] + "..."

    def _postprocess_answer(self, answer: str) -> str:
        cleaned = answer.strip()

        # Supprime certains préfixes fréquents des petits modèles.
        prefixes = (
            "Réponse :",
            "Voici la réponse :",
            "Bien sûr.",
            "Bien sûr,",
        )

        for prefix in prefixes:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()

        return cleaned

    def _normalize(self, text: str) -> str:
        text = text.lower()
        text = unicodedata.normalize("NFD", text)
        text = "".join(char for char in text if unicodedata.category(char) != "Mn")
        return f" {text} "
