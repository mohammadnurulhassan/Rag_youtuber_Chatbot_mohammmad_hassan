
import streamlit as st
import requests
from pathlib import Path

API_URL = "http://127.0.0.1:8000/rag/query"

ASSETS_PATH = Path(__file__).resolve().parents[1] / "assets"
AVATAR_PATH = ASSETS_PATH / "data_engineer.png"


def layout():
    st.set_page_config(page_title="Youtuber RAG Chatbot", layout="wide")

    # Header with avatar
    col1, col2 = st.columns([1, 3])
    with col1:
        if AVATAR_PATH.exists():
            st.image(AVATAR_PATH, caption="Data Engineer", use_column_width=True)
    with col2:
        st.title("🎓 Youtuber RAG Chatbot")
        st.markdown(
            "Ställ frågor om föreläsningar från min data engineering YouTube-kanal.\n\n"
            "Botten svarar baserat på transkriptionerna i kunskapsbasen."
        )

    st.markdown("---")

    if "history" not in st.session_state:
        st.session_state["history"] = []

    user_input = st.text_input("Skriv din fråga här:")

    if st.button("Skicka") and user_input.strip():
        # spara användarens fråga
        st.session_state["history"].append(("user", user_input))

        # 🛡️ Skydd: hantera koppling till backend + JSON-fel
        try:
            response = requests.post(API_URL, json={"prompt": user_input}, timeout=20)
        except requests.exceptions.RequestException as e:
            st.error(f"Kunde inte nå backend API:t ({API_URL}).\n\nFel: {e}")
            return

        # Kontrollera statuskod
        if response.status_code != 200:
            st.error(
                f"Backend svarade med statuskod {response.status_code}.\n\n"
                f"Body:\n\n{response.text}"
            )
            return

        # Försök tolka JSON – fånga JSONDecodeError
        try:
            data = response.json()
        except Exception as e:
            st.error(
                "Kunde inte tolka backend-svaret som JSON.\n\n"
                f"Fel: {e}\n\n"
                f"Raw response:\n\n{response.text}"
            )
            return

        # Nu ska data ha nycklarna: answer, filename, filepath
        answer = data.get("answer", "(ingen answer-nyckel i JSON)")
        source_file = data.get("filename", "")
        source_path = data.get("filepath", "")

        st.session_state["history"].append(
            (
                "bot",
                f"{answer}\n\n_Källa: {source_file}_\n\n`{source_path}`",
            )
        )

    st.markdown("## Konversation")
    for role, text in st.session_state["history"]:
        if role == "user":
            st.markdown(f"**Du:** {text}")
        else:
            st.markdown(f"**Bot:** {text}")


if __name__ == "__main__":
    layout()
