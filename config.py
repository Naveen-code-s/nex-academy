import os
from dotenv import load_dotenv

load_dotenv()


# ==========================================
# API CONFIGURATION
# ==========================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ==========================================
# AI CONFIGURATION
# ==========================================

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "llama-3.3-70b-versatile"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================
# RAG CONFIGURATION
# ==========================================

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 150

TOP_K = 5


# ==========================================
# FILE CONFIGURATION
# ==========================================

UPLOAD_DIR = "data/uploads"

PROCESSED_DIR = "data/processed"