from pathlib import Path
import os
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")

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


# Local LLM generation with Ollama
OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
OLLAMA_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "90"))
OLLAMA_MAX_CONTEXT_CHARS = int(os.getenv("OLLAMA_MAX_CONTEXT_CHARS", "6000"))
