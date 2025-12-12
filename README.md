# Rag_youtuber_Chatbot_mohammmad_hassan
 Create a RAG_chatbot on real world scenario. 
# Youtuber RAG Chatbot – Data Engineering Knowledge Assistant

This project is a Retrieval-Augmented Generation (RAG) chatbot built for data engineering learning content.
The chatbot answers questions based on  YouTube lecture transcriptS and notes, stored as Markdown files.
It combines vector search with LLM reasoning and is deployed with Azure Function App support.

----

### 🚀 Project Highlights

- 📚 Knowledge base built from Markdown (.md) lecture notes

- 🔍 Vector search using LanceDB

- 🧠 RAG pipeline using PydanticAI + Gemini

- ⚡ FastAPI backend

 - 💬 Streamlit frontend with chat UI

- ☁️ Connected to Azure Function App

- 🔐 Robust error handling for LLM/API failures

-----

### 📂 Project Structure
```
Rag_youtuber_Chatbot_mohammmad_hassan/
│
├── backend/
│   ├── rag.py
│   ├── data_models.py
│   └── constants.py
│
├── frontend/
│   └── app.py
│
├── data/               # Markdown knowledge base
├── assets/             # Images & avatars
├── ingestion.py
├── api.py
├──function_app.py
├── README.md
└── requirements.txt
```
----
### ▶️ How to Run the Project Locally

#### 1️⃣ Create and activate virtual environment & Install dependencies
```
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
```
#### 2️⃣ Set environment variables & Ingest Markdwon files into vector database
```
GOOGLE_API_KEY=api_key_here
python ingestion.py
```

 This will:
- Read .md files from the data/ folder
- Create embeddings
- Store them in LanceDB

#### 3️⃣ Start the backend (FastAPI)
```
uv run uvicorn api:app --reload
```

Backend will be available at:
- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

#### 4️⃣ Start the frontend (Streamlit)

```
  uv run streamlit run frontend/app.py
```
Frontend will open at:

- http://localhost:8501

----
### Azure Deployment

- Backend connected to Azure Function App

- Enables cloud execution of the RAG API

- Same FastAPI logic, Azure-hosted endpoint
---
### 🖼️ Screenshots
#### Rag_bot UI
![Rag UI](/assets/rag_UI.png)

#### RAG Answer with Source
![Conversation](/assets/conversation.png)





