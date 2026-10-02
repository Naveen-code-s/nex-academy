from rag.pipeline import answer_question


def research_agent(
    vector_store,
    question
):

    answer, documents = answer_question(
        vector_store,
        question
    )

    return {
        "type": "research",
        "answer": answer,
        "documents": documents
    }