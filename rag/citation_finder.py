def find_citations(vector_store, claim, top_k=5):
    """
    Find relevant source passages for a research claim.
    """

    if not claim or not claim.strip():
        return []

    results = vector_store.similarity_search(
        claim,
        k=top_k
    )

    citations = []

    for document in results:
        metadata = document.metadata

        citations.append(
            {
                "source": metadata.get(
                    "source",
                    "Unknown"
                ),
                "page": metadata.get(
                    "page",
                    "N/A"
                ),
                "content": document.page_content
            }
        )

    return citations