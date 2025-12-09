from pydantic_ai import Agent
from backend.data_models import RagResponse
from backend.constants import VECTOR_DATABASE_PATH
import lancedb

vector_db = lancedb.connect(uri=VECTOR_DATABASE_PATH)

rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=(
        "You are a helpful teaching assistant for a data engineering "
        "YouTube channel. Answer questions based ONLY on the provided "
        "lecture transcript context. If something is not in the context, "
        "say that you don't know.",
    ),
    output_type=RagResponse,
)

@rag_agent.tool_plain
def retrieve_top_documents(query: str, k=3) -> str:
    """
    Uses vector search to find the closest k matching documents to the query
    """
    results = vector_db["articles"].search(query=query).limit(k).to_list()
    top_result = results[0]

    return f"""
    Filename: {top_result["filename"]},

    Filepath: {top_result["filepath"]},

    Content: {top_result["content"]}
    """