import streamlit as st
import requests
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()


API_URL = f"https://youtuber-ragbot.azurewebsites.net//rag/query?code={os.getenv('FUNCTION_APP_API')}"

BASE_DIR = Path(__file__).absolute().parents[1]
ASSETS_PATH = BASE_DIR / "assets"

AVATAR_PATH = ASSETS_PATH / "data_engineer.png"



def call_backend(prompt: str) -> dict:
    """Call the FastAPI RAG backend and return JSON or raise."""
    response = requests.post(API_URL, json={"prompt": prompt}, timeout=30)

    if response.status_code != 200:
    
        raise RuntimeError(
            f"Backend returned {response.status_code}.\n\nBody:\n{response.text}"
        )

    try:
        data = response.json()
    except Exception as e:  
        raise RuntimeError(
            f"Could not parse backend response as JSON.\nError: {e}\n\nRaw:\n{response.text}"
        )

    return data


def render_message(role: str, text: str):
    """Simple chat-style rendering."""
    if role == "user":
        st.markdown(
            f"""
            <div style="
                background-color:#E8F4FF;
                padding:0.6rem 0.8rem;
                border-radius:0.6rem;
                margin-bottom:0.5rem;
                border:1px solid #BBD9FF;
            ">
                <strong>You:</strong><br>{text}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="
                background-color:#F7F7F9;
                padding:0.6rem 0.8rem;
                border-radius:0.6rem;
                margin-bottom:0.5rem;
                border:1px solid #DDDEE5;
            ">
                <strong>Data_Bot:</strong><br>{text}
            </div>
            """,
            unsafe_allow_html=True,
        )




# =================================================================
#                               Main layout
# ==================================================
def layout():
    st.set_page_config(page_title=" RAG_Chatbot", layout="wide")

    # ---------- HEADER ----------
    header_col1, header_col2 = st.columns([1, 2])

    with header_col1:
        if AVATAR_PATH.exists():
            st.image(
                AVATAR_PATH,
                caption="Your Data Engineer RAG Assistant",
                use_container_width=True,
            )

    with header_col2:
        st.title("🎓  RAG CHATBOT")
        st.markdown(
            """
                Ask anything about **Data engineering**, the **Modern data stack**, **Snowflake**, **DBT**,  
                data pipelines, and related topics.  
                This chatbot generates answers using the transcripts  and notes stored in your knowledge base.
            """

        )
      

    st.markdown("---")

    # ---------- SIDEBAR ----------
    with st.sidebar:
        st.subheader("ℹ️ About this chatbot")
        st.write(
            """
            • Backend: **FastAPI + PydanticAI + LanceDB**  
            • Frontend: **Streamlit**  
            • Knowledge base: Pre-loaded `.md` files (YouTube lecture notes).
            """
        )
        st.write("We can update the knowledge base by adding more `.md` files.")

    # ---------- SESSION STATE ----------
    if "history" not in st.session_state:
    
        st.session_state["history"] = []


    # ---------- INPUT AREA ----------
    with st.container():
        st.markdown("## 💬 Ask your question")
        user_input = st.text_input(
            "Type your question here:",
            placeholder="e.g. What is dbt and why do we use it in the modern data stack?",
        )

        send_col1, send_col2 = st.columns([1, 4])
        with send_col1:
            send_clicked = st.button("Send", type="primary")

    # ---------- HANDLE NEW MESSAGE ----------
    if send_clicked and user_input.strip():
        
        st.session_state["history"].append(("user", user_input))

        
        try:
            data = call_backend(user_input)
        except Exception as e:
            
            st.session_state["history"].append(
                ("bot", f"⚠️ An error occurred when calling the backend:\n\n`{e}`")
            )
        else:
            answer = data.get("answer", "(no 'answer' key in JSON)")
            source_file = data.get("filename", "")
            source_path = data.get("filepath", "")

            bot_text = (
                f"{answer}\n\n"
                f"_Source: **{source_file}**"
                f"`{source_path}`"

            )

            st.image(ASSETS_PATH/f"{source_file}.png", caption="Related image", use_container_width=True)

            st.session_state["history"].append(("bot", bot_text))


    # ---------- CHAT HISTORY ----------
    st.markdown("## 🧠 Conversation")
    for role, text in st.session_state["history"]:
        render_message(role, text)

        
        if role == "Data_bot":
        
            if "_Source:" in text:
            
                try:
                
                    start = text.index("**") + 2
                    end = text.index("**", start)
                    src_filename = text[start:end]
                    
                except Exception:
                
                    pass


if __name__ == "__main__":
    layout()
