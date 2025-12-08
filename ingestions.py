# ingestion.py
from backend.constants import VECTOR_DATABASE_PATH, DATA_PATH
import lancedb
from backend.data_models import TranscriptDoc
from pathlib import Path


def setup_vector_db(path: Path):
    """Create (or open) the LanceDB vector database."""
    path.mkdir(exist_ok=True)
    vector_db = lancedb.connect(uri=path)
    vector_db.create_table("transcripts", schema=TranscriptDoc, exist_ok=True)
    return vector_db


def ingest_docs_to_vector_db(table):
    """
    Ingest all .md (and optionally .txt) transcript files into LanceDB.

    For each file:
      - compute doc_id from stem
      - delete any old row with same doc_id (upsert behaviour)
      - add a new row with content
    LanceDB will generate embeddings automatically because of TranscriptDoc schema.
    """
    # Change this if you want to support other extensions
    patterns = ["*.md", "*.txt"]

    for pattern in patterns:
        for file in DATA_PATH.glob(pattern):
            content = file.read_text(encoding="utf-8")

            doc_id = file.stem

            # Remove any old version of this doc_id
            table.delete(f"doc_id = '{doc_id}'")

            # Add the new document
            table.add(
                [
                    {
                        "doc_id": doc_id,
                        "filepath": str(file.resolve()),
                        "filename": file.stem,
                        "content": content,
                    }
                ]
            )

            print(f"Ingested: {file.name} → doc_id={doc_id}")
    print("Current table shape:", table.to_pandas().shape)


if __name__ == "__main__":
    vector_db = setup_vector_db(VECTOR_DATABASE_PATH)
    ingest_docs_to_vector_db(vector_db["transcripts"])
