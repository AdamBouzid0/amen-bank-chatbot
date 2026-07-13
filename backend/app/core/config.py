from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Mock banking data
DATA_MOCK_DIR = PROJECT_ROOT / "data" / "mock"

# RAG data paths
RAG_CHUNKS_PATH = PROJECT_ROOT / "data" / "processed" / "chunks.jsonl"
RAG_DOCUMENTS_PATH = PROJECT_ROOT / "data" / "processed" / "documents.jsonl"
RAG_REJECTED_CHUNKS_PATH = PROJECT_ROOT / "data" / "processed" / "rejected_chunks.jsonl"

RAG_VECTORSTORE_PATH = PROJECT_ROOT / "data" / "vectorstore" / "chroma"

# RAG settings
RAG_COLLECTION_NAME = os.getenv(
    "RAG_COLLECTION_NAME",
    "amen_bank_rag_v1",
)

RAG_EMBEDDING_MODEL = os.getenv(
    "RAG_EMBEDDING_MODEL",
    "intfloat/multilingual-e5-small",
)

RAG_TOP_K = int(os.getenv("RAG_TOP_K", "4"))

RAG_EMBEDDING_BATCH_SIZE = int(
    os.getenv("RAG_EMBEDDING_BATCH_SIZE", "32")
)
