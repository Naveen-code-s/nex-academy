from search.global_search import global_search


def search_agent(
    vector_store,
    query
):

    results, answer = global_search(
        vector_store,
        query
    )

    return {
        "type": "search",
        "answer": answer,
        "documents": results
    }