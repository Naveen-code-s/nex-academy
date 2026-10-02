from core.prompts import GLOBAL_SEARCH_PROMPT
from core.llm import get_llm


def global_search(
    vector_store,
    query,
    top_k=10,
):

    if not query.strip():

        return [], "Please enter a search query."

    results = vector_store.similarity_search(
        query,
        k=top_k,
    )

    if not results:

        return [], "No relevant information found."

    context_parts = []

    for document in results:

        source = document.metadata.get(
            "source",
            "Unknown",
        )

        page = document.metadata.get(
            "page",
            "N/A",
        )

        context_parts.append(
            f"""
Source: {source}

Page: {page}

Content:

{document.page_content}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = GLOBAL_SEARCH_PROMPT.format(
        query=query,
        context=context,
    )

    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    return results, response.content