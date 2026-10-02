def generate_citations(documents):
    """
    Generate source citations from retrieved documents.
    """

    citations = []

    if not documents:
        return citations

    for document in documents:

        metadata = document.metadata

        citations.append(
            {
                "source": metadata.get(
                    "source",
                    "Unknown source"
                ),

                "page": metadata.get(
                    "page",
                    "N/A"
                ),

                "content": document.page_content
            }
        )

    return citations