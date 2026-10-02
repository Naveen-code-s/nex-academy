from config import TOP_K


def get_retriever(vector_store):
    """
    Create a retriever from the FAISS vector store.
    """

    return vector_store.as_retriever(
        search_kwargs={
            "k": TOP_K
        }
    )
    