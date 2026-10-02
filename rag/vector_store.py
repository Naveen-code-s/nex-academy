from langchain_community.vectorstores import FAISS

from core.embeddings import get_embeddings


def create_vector_store(documents):
    """
    Create a FAISS vector database from document chunks.
    """

    if not documents:
        raise ValueError(
            "No documents available for indexing."
        )

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    return vector_store
