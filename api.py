
from fastapi import FastAPI , HTTPException
from backend.data_models import Prompt, RagResponse
from backend.rag import rag_agent
from pydantic_ai.exceptions import ModelHTTPError

app = FastAPI()





@app.get("/")
async def hello_message():
    return {"test": "hello"}


@app.post("/rag/query")
async def query_documentation(query: Prompt):
    try:
    
        result = await rag_agent.run(query.prompt)

        return result.output

    except ModelHTTPError as e:
    
        if getattr(e, "status_code", None) == 429:
    
            raise HTTPException(
                status_code=503,
                detail="Gemini LLM quota exceeded. Please try again later or switch model/plan."
            )
        raise HTTPException(
            status_code=500,
            detail=f"LLM backend error: {str(e)}"
        )
