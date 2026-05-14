import os
from typing import Any

import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


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
            timeout=10,
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
            "message": "Le backend met trop de temps à répondre.",
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


def display_metadata(metadata: dict[str, Any]) -> None:
    intent = metadata.get("intent")
    requires_confirmation = metadata.get("requires_confirmation")
    error = metadata.get("error")
    data = metadata.get("data")
    pending_action = metadata.get("pending_action")

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
        "Prototype de stage basé sur des données fictives, une API bancaire simulée "
        "et un routeur d'intention par règles."
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
