# backend/rag.py
import os
from typing import Tuple

import lancedb
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

from backend.constants import VECTOR_DATABASE_PATH
from backend.data_models import TranscriptDoc, RagResponse

load_dotenv()

# 1. Connect to LanceDB
db = lancedb.connect(VECTOR_DATABASE_PATH)
TRANSCRIPTS_TABLE_NAME = "transcripts"


def get_transcripts_table():
    return db.open_table(TRANSCRIPTS_TABLE_NAME)


def retrieve_relevant_doc(question: str) -> Tuple[TranscriptDoc, str]:
    """
    Use LanceDB to find the most relevant transcript for the user's question.
    Returns (TranscriptDoc, context_text).
    Because TranscriptDoc has embedding_model, we can search with a string.
    """
    table = get_transcripts_table()
    # search with raw text; LanceDB embeds internally using the model in TranscriptDoc
    result_df = table.search(question).limit(1).to_pydantic(TranscriptDoc)

    if not result_df:
        # fallback: no document
        empty_doc = TranscriptDoc(
            doc_id="",
            filepath="",
            filename="",
            content="",
            embedding=[0.0] * 3072,
        )
        return empty_doc, ""

    doc = result_df[0]
    context = doc.content
    return doc, context


# 2. Configure PydanticAI model
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    raise RuntimeError("GOOGLE_API_KEY not set in environment.")

model = GeminiModel(
    model_name="gemini-2.5-flash",
    api_key=google_api_key,
)

# 3. Define the agent
rag_agent = Agent(
    model=model,
    system_prompt=(
        "You are a helpful teaching assistant for a data engineering "
        "YouTube channel. Answer questions based ONLY on the provided "
        "lecture transcript context. If something is not in the context, "
        "say that you don't know."
    ),
)


@rag_agent.tool
def get_transcript_context(question: str) -> RagResponse:
    """
    Tool used by the agent to fetch the most relevant transcript and answer.
    It combines:
      - vector search (LanceDB)
      - LLM generation on top of that context
    """
    doc, context = retrieve_relevant_doc(question)

    if not context:
        return RagResponse(
            filename="",
            filepath="",
            answer=(
                "Jag hittade ingen relevant föreläsningstranskription i databasen "
                "för den här frågan."
            ),
        )

    # Build a prompt using the transcript as context
    prompt = f"""
You are a teaching assistant answering questions about data engineering lectures.

Here is a transcript from the YouTube lecture:

\"\"\"{context}\"\"\"

User question:
\"\"\"{question}\"\"\"

Answer in a clear, structured way, step by step.
If something is missing from the transcript, say that you don't know based on this lecture.
"""

    # We call the underlying model directly here for clarity
    result = model.run(prompt)

    return RagResponse(
        filename=doc.filename,
        filepath=doc.filepath,
        answer=result.output_text,  # adjust attribute name if needed
    )
