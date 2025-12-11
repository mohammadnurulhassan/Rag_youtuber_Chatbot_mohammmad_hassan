
from fastapi import FastAPI
from backend.data_models import Prompt, RagResponse
from backend.rag import rag_agent
from pydantic_ai.exceptions import ModelHTTPError

app = FastAPI()


@app.get("/test")
async def test():
    return {"status": "ok"}


@app.post("/rag/query")
async def query_documentation(query: Prompt):
    
    result = await rag_agent.run(query.prompt)
        
    
        
    return result.output