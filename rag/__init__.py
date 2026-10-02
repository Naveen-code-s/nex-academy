from pathlib import Path

from rag.document_loader import load_document
from rag.chunker import split_documents


def test_document_loading():

    test_file = Path("data/uploads/test.txt")

    test_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    test_file.write_text(
        "NEXUS AI is an enterprise AI research assistant.",
        encoding="utf-8"
    )

    documents = load_document(
        str(test_file)
    )

    assert len(documents) > 0
    assert "NEXUS AI" in documents[0].page_content


def test_chunking():

    test_file = Path("data/uploads/test.txt")

    documents = load_document(
        str(test_file)
    )

    chunks = split_documents(documents)

    assert len(chunks) > 0
    