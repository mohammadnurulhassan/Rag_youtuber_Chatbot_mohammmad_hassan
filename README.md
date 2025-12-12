
# Youtuber RAG Chatbot – Data Engineering Knowledge Assistant

This project is a Retrieval-Augmented Generation (RAG) chatbot built for data engineering learning content.
The chatbot answers questions based on  YouTube lecture transcripts and notes, stored as Markdown files.
It combines vector search with LLM reasoning and is deployed with Azure Function App support.

----

### 🚀 Project Highlights

- Ingests **Markdown transcripts** from YouTube lectures

- Generates **embeddings** and stores them in **LanceDB**

- Retrieves relevant content using **vector similarity**

- Generates grounded answers using **LLM + retrieved context**

- Provides a **Streamlit chat UI**

- Exposes a **FastAPI backend**, deployable via **Azure Function App**

-----

### 🧱 Architecture
```
Markdown files (.md)
        ↓
Ingestion & Embeddings
        ↓
     LanceDB
        ↓
FastAPI (RAG logic)
        ↓
Streamlit Frontend
        ↓
     End User

```
----
### ▶️ How to Run the Project Locally

```
# 1. Create environment
uv venv
source .venv/Scripts/activate

# 2. Install dependencies
uv init

# 3. Run ingestion
python ingestion.py

# 4. Start backend
uv run uvicorn api:app --reload

# 5. Start frontend
uv run streamlit run frontend/app.py

```

----
### ☁️ Azure Deployment

- Backend connected to Azure Function App

- Enables cloud execution of the RAG API

- Same FastAPI logic, Azure-hosted endpoint
---
### 🖼️ Screenshots

### Swagger UI
![FastAPI](/assets/swagger_ui.png)

#### Rag_bot UI
![Rag UI](/assets/rag_UI.png)

#### RAG Answer with Source
![Conversation](/assets/conversation.png)



----

### ✅ Learning Outcomes

- Built a full RAG pipeline from scratch

- Used vector databases in practice

- Integrated LLMs with structured retrieval

- Designed a clean frontend for AI applications
  
----
## 👤 Author

**Mohammad Nurul Hassan**
  Data Engineering Student





