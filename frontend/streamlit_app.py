import os
from typing import Any

import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
CHAT_API_TIMEOUT = int(os.getenv("CHAT_API_TIMEOUT", "60"))


st.set_page_config(
    page_title="AMENet Chatbot Assistant",
    page_icon="💬",
    layout="wide",
)


def get_welcome_message() -> dict[str, Any]:
    return {
        "role": "assistant",
        "content": (
            "Bonjour, je suis votre assistant bancaire AMENet. "
            "Je peux vous aider à consulter un solde fictif, afficher des opérations, "
            "préparer un virement, faire une opposition carte, demander un document, "
            "commander un chéquier ou simuler un crédit."
        ),
        "metadata": None,
    }


def call_health_api() -> bool:
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def call_chat_api(message: str, client_id: str) -> dict[str, Any]:
    url = f"{API_BASE_URL}/chat"

    try:
        response = requests.post(
            url,
            json={
                "message": message,
                "client_id": client_id,
            },
            timeout=CHAT_API_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        return {
            "message": (
                "Impossible de contacter le backend FastAPI. "
                "Vérifiez que le serveur est lancé sur http://127.0.0.1:8000."
            ),
            "intent": "connection_error",
            "requires_confirmation": False,
            "data": {},
            "sources": [],
            "error": "connection_error",
        }

    except requests.exceptions.Timeout:
        return {
            "message": "Le backend met trop de temps à répondre. Le premier appel RAG peut être plus long car le modèle d’embeddings se charge en mémoire.",
            "intent": "timeout",
            "requires_confirmation": False,
            "data": {},
            "sources": [],
            "error": "timeout",
        }

    except requests.exceptions.RequestException as error:
        return {
            "message": f"Erreur lors de l'appel au backend : {error}",
            "intent": "request_error",
            "requires_confirmation": False,
            "data": {},
            "sources": [],
            "error": str(error),
        }


def initialize_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [get_welcome_message()]

    if "client_id" not in st.session_state:
        st.session_state.client_id = "C001"


def reset_conversation() -> None:
    st.session_state.messages = [get_welcome_message()]


def handle_user_message(prompt: str) -> None:
    if not prompt.strip():
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
            "metadata": None,
        }
    )

    with st.spinner("Le chatbot réfléchit..."):
        response = call_chat_api(
            message=prompt,
            client_id=st.session_state.client_id,
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.get("message", "Aucune réponse reçue."),
            "metadata": response,
        }
    )


def display_sidebar() -> None:
    st.sidebar.title("AMENet Chatbot")

    backend_ok = call_health_api()

    if backend_ok:
        st.sidebar.success("Backend connecté")
    else:
        st.sidebar.error("Backend indisponible")

    st.sidebar.markdown("---")

    st.sidebar.selectbox(
        "Client fictif",
        options=["C001", "C002"],
        format_func=lambda client_id: {
            "C001": "C001 - Société Démo SARL",
            "C002": "C002 - Client Particulier Démo",
        }.get(client_id, client_id),
        key="client_id",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Exemples rapides")

    examples = [
        "Quel est mon solde ?",
        "Affiche mes dernières opérations",
        "Je veux faire un virement de 500 DT",
        "Je veux bloquer ma carte qui termine par 4582",
        "Je veux commander un chéquier",
        "Je veux demander un relevé",
        "Simule un crédit de 20000 DT sur 5 ans",
        "Comment faire opposition à une carte ?",
        "Quels services sont disponibles sur AMENet ?",
        "Quelles actions nécessitent une confirmation ?",
        "Je n'arrive pas à me connecter à AMENet",
    ]

    for index, example in enumerate(examples):
        if st.sidebar.button(example, key=f"example_{index}"):
            handle_user_message(example)
            st.rerun()

    st.sidebar.markdown("---")

    if st.sidebar.button("Réinitialiser la conversation"):
        reset_conversation()
        st.rerun()

    st.sidebar.caption(f"API : {API_BASE_URL}")


def display_rag_sources(sources: list[dict[str, Any]]) -> None:
    if not sources:
        return

    with st.expander("Sources documentaires utilisées", expanded=True):
        for index, source in enumerate(sources, start=1):
            title = source.get("title", "Source sans titre")
            source_file = source.get("source_file")
            source_image = source.get("source_image")
            page = source.get("page")
            score = source.get("score")

            st.markdown(f"**{index}. {title}**")

            details = []

            if source_file:
                details.append(f"Fichier : `{source_file}`")

            if page is not None:
                details.append(f"Page : `{page}`")

            if source_image:
                details.append(f"Capture : `{source_image}`")

            if score is not None:
                details.append(f"Score : `{score:.3f}`")

            if details:
                st.caption(" • ".join(details))


def display_metadata(metadata: dict[str, Any]) -> None:
    intent = metadata.get("intent")
    requires_confirmation = metadata.get("requires_confirmation")
    error = metadata.get("error")
    data = metadata.get("data")
    pending_action = metadata.get("pending_action")
    sources = metadata.get("sources") or []

    display_rag_sources(sources)

    if requires_confirmation:
        st.warning("Cette action nécessite une confirmation explicite.")

    with st.expander("Détails techniques", expanded=False):
        st.write("Intent :", intent)
        st.write("Confirmation requise :", requires_confirmation)

        if pending_action:
            st.write("Action en attente :")
            st.json(pending_action)

        if data:
            st.write("Données :")
            st.json(data)

        if error:
            st.error(error)


def display_confirmation_buttons(message_index: int) -> None:
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("Confirmer", key=f"confirm_{message_index}", type="primary"):
            handle_user_message("oui")
            st.rerun()

    with col2:
        if st.button("Annuler", key=f"cancel_{message_index}"):
            handle_user_message("non")
            st.rerun()


def display_messages() -> None:
    last_index = len(st.session_state.messages) - 1

    for index, message in enumerate(st.session_state.messages):
        role = message["role"]
        content = message["content"]
        metadata = message.get("metadata")

        with st.chat_message(role):
            st.markdown(content)

            if metadata:
                display_metadata(metadata)

                is_last_message = index == last_index
                is_assistant_message = role == "assistant"
                needs_confirmation = metadata.get("requires_confirmation") is True

                if is_last_message and is_assistant_message and needs_confirmation:
                    display_confirmation_buttons(index)


def display_header() -> None:
    st.title("Chatbot assistant bancaire AMENet")
    st.caption(
        "Prototype de stage basé sur des données fictives, une API bancaire simulée, "
        "un routeur d'intention et un module RAG documentaire."
    )

    st.info(
        "Les opérations bancaires sont simulées. Aucune donnée réelle n'est utilisée "
        "et aucune opération réelle n'est exécutée."
    )


def main() -> None:
    initialize_session_state()
    display_sidebar()
    display_header()
    display_messages()

    prompt = st.chat_input("Écrivez votre message...")

    if prompt:
        handle_user_message(prompt)
        st.rerun()


if __name__ == "__main__":
    main()
