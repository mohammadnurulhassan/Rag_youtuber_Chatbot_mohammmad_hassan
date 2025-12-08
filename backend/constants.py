# backend/constants.py
from pathlib import Path

# Root = project root (where 10_pydanticai_rags or similar lives)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Folder with your .md transcript files
DATA_PATH = PROJECT_ROOT / "data"

# Folder where LanceDB will store the vector database
VECTOR_DATABASE_PATH = PROJECT_ROOT / "Language_model"
# Folder where temporary files can be stored