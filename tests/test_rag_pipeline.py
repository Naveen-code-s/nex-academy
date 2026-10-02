from pathlib import Path

from rag.document_loader import load_document
from rag.chunker import split_documents
from rag.vector_store import create_vector_store
from rag.retriever import get_retriever


def test_rag_vector_search():

    # Create test document
    test_file = Path("data/uploads/rag_test.txt")

    test_file.write_text(
        """
        NEXUS AI is an enterprise artificial intelligence platform.
        It supports document analysis, semantic search, and
        retrieval augmented generation.
        The platform can answer questions using uploaded documents.
        """,
        encoding="utf-8"
    )

    # 1. Load
    documents = load_document(
        str(test_file)
    )

    assert len(documents) > 0

    # 2. Chunk
    chunks = split_documents(documents)

    assert len(chunks) > 0

    # 3. Create vector store
    vector_store = create_vector_store(chunks)

    assert vector_store is not None

    # 4. Retrieve
    retriever = get_retriever(vector_store)

    results = retriever.invoke(
        "What is NEXUS AI?"
    )

    assert len(results) > 0

    # 5. Check relevant content
    combined_text = " ".join(
        document.page_content
        for document in results
    )

    assert "NEXUS AI" in combined_text