# Youtuber RAG Chatbot – Data Engineering Knowledge Assistant

This project is a Retrieval-Augmented Generation (RAG) chatbot built for data engineering learning content.
The chatbot answers questions based on my own YouTube lecture transcriptions and notes, stored as Markdown files.
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
├── README.md
└── requirements.txt
```
