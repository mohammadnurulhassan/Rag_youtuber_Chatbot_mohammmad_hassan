# backend/data_models.py
from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

# Use LanceDB's built-in Gemini text embedding model
embedding_model = (
    get_registry()
    .get("gemini-text")
    .create(name="gemini-embedding-001")
)

# Gemini text embedding dimension
EMBEDDING_DIM = 3072


class TranscriptDoc(LanceModel):
    """One YouTube lecture / video transcript in the knowledge base."""

    doc_id: str
    filepath: str
    filename: str = Field(
        description="stem of the file (without suffix), usually video id or slug"
    )
    # content is the raw transcript text
    content: str = embedding_model.SourceField()
    # embedding vector generated automatically by LanceDB
    embedding: Vector(EMBEDDING_DIM) = embedding_model.VectorField()


class Prompt(BaseModel):
    """User query to the RAG system."""
    prompt: str = Field(
        description="Prompt from user. If empty, treat as missing.",
        min_length=1,
    )


class RagResponse(BaseModel):
    """What we send back to frontend."""
    filename: str = Field(
        description="filename (stem) of the most relevant transcript file"
    )
    filepath: str = Field(
        description="absolute path to the retrieved transcript file"
    )
    answer: str = Field(
        description="LLM answer based primarily on the retrieved transcript"
    )
