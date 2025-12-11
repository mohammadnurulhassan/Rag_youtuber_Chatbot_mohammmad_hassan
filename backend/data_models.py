from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()


embedding_model =(
    get_registry()
    .get("gemini-text")
    .create(name="gemini-embedding-001")
)

EMBEDDING_DIM = 3072  

class Article(LanceModel):
    """
    One row per transcript/file in the knowledge base.
    """
    doc_id: str
    filepath: str
    filename: str = Field(
        description="The stem of the file, without extension (e.g. 'Modern data stack-dockerize your data pipeline')"
    )
    content: str = embedding_model.SourceField()
    embedding: Vector(EMBEDDING_DIM) = embedding_model.VectorField()


class Prompt(BaseModel):
    prompt: str = Field(
        description="Prompt from user, if empty consider prompt as missing"
    )


class RagResponse(BaseModel):
    filename: str = Field(
        description="Filename of the retrieved file without suffix"
    )
    filepath: str = Field(
        description="Absolute path to the retrieved file"
    )
    answer: str = Field(
        description="Answer based on the retrieved file(s)"
    )
