# api.py
from fastapi import FastAPI
from backend.data_models import Prompt, RagResponse
from backend.rag import rag_agent

app = FastAPI(title="Youtuber RAG API")


@app.get("/test")
async def test():
    return {"status": "ok", "message": "Youtuber RAG API up and running"}


@app.post("/rag/query", response_model=RagResponse)
async def query_documentation(query: Prompt) -> RagResponse:
    """
    Main RAG endpoint:
      - Takes a user prompt (query.prompt)
      - Uses our PydanticAI rag_agent to answer
      - Returns RagResponse (answer + filename + filepath)
    """
    # Depending on pydantic_ai version, use run() or arun()
    # Here we assume async arun is available:
    result = await rag_agent.arun(query.prompt)
    # result.data (or result.output) should be the RagResponse
    return result.data
