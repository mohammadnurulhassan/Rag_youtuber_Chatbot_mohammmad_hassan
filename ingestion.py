# ingestion.py
from pathlib import Path
import time

import lancedb

from backend.constants import VECTOR_DATABASE_PATH, DATA_PATH
from backend.data_models import Article  # uses gemini-embedding-001


def setup_vector_db(path: Path | str):
    path = Path(path)
    path.mkdir(exist_ok=True)

    db = lancedb.connect(str(path))

    # 💣 IMPORTANT: if 'articles' exists with old schema (768-dim), drop it
    if "articles" in db.table_names():
        print("Dropping old 'articles' table to reset schema...")
        db.drop_table("articles")

    print("Creating fresh 'articles' table with Article schema...")
    table = db.create_table("articles", schema=Article, exist_ok=False)

    return db, table


def ingest_docs_to_vector_db(table):
    TEXT_EXTENSIONS = {".md", ".txt"}

    for file in DATA_PATH.iterdir():
        if file.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        doc_id = file.stem

        # not needed anymore since we dropped table, but safe to keep:
        table.delete(f"doc_id = '{doc_id}'")

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

        print("Ingested:", file.name)
        print(table.to_pandas()[["doc_id", "filename"]])
        time.sleep(0.1)


if __name__ == "__main__":
    print("VECTOR_DATABASE_PATH:", VECTOR_DATABASE_PATH)
    print("DATA_PATH:", DATA_PATH)

    db, table = setup_vector_db(VECTOR_DATABASE_PATH)
    ingest_docs_to_vector_db(table)

    print("\nDone. Tables:", db.table_names())
    print("Schema:\n", table.schema)
