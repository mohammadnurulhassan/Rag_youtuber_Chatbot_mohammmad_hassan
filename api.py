# api.py
from fastapi import FastAPI
from backend.data_models import Prompt, RagResponse

app = FastAPI(title="Youtuber RAG API")


@app.get("/test")
async def test():
    return {"status": "ok", "message": "Youtuber RAG API up and running"}


@app.post("/rag/query", response_model=RagResponse)
async def query_documentation(query: Prompt) -> RagResponse:
    """
    TEMPORARY SIMPLE IMPLEMENTATION:
    Just echo back the prompt and a fake filename.
    This guarantees that the response is valid JSON and matches RagResponse.
    """
    return RagResponse(
        filename="dummy_transcript",
        filepath="/path/to/dummy_transcript.md",
        answer=f"(TEMP) Du frågade: {query.prompt}",
    )
