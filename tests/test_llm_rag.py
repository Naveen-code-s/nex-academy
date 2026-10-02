from pathlib import Path

from rag.document_loader import load_document
from rag.chunker import split_documents
from rag.vector_store import create_vector_store
from rag.pipeline import answer_question


def test_full_rag_pipeline():

    test_file = Path("data/uploads/llm_test.txt")

    test_file.write_text(
        """
        NEXUS AI is an enterprise artificial intelligence platform.
        It provides document analysis and semantic search.
        NEXUS AI uses Retrieval Augmented Generation to answer
        questions from uploaded documents.
        """,
        encoding="utf-8"
    )

    # Load document
    documents = load_document(
        str(test_file)
    )

    # Create chunks
    chunks = split_documents(documents)

    # Create vector database
    vector_store = create_vector_store(chunks)

    # Ask question
    answer, sources = answer_question(
        vector_store,
        "What is NEXUS AI?"
    )

    # Validate answer
    assert answer is not None
    assert len(answer.strip()) > 0

    # Validate retrieved sources
    assert len(sources) > 0

    # Validate source metadata
    assert sources[0].metadata["source"] == "llm_test.txt"
    