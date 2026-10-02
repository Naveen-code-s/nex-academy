from core.llm import get_llm
from core.prompts import RAG_SYSTEM_PROMPT
from rag.retriever import get_retriever


def answer_question(vector_store, question):
    """
    Retrieve relevant documents and generate
    an answer using the LLM.
    """

    if not question.strip():
        raise ValueError(
            "Question cannot be empty."
        )

    retriever = get_retriever(vector_store)

    documents = retriever.invoke(question)

    if not documents:
        return (
            "I could not find relevant information "
            "in the uploaded documents.",
            []
        )

    context_parts = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown"
        )

        page = document.metadata.get(
            "page",
            "N/A"
        )

        context_parts.append(
            f"""
Source: {source}
Page: {page}

Content:
{document.page_content}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = RAG_SYSTEM_PROMPT.format(
        context=context,
        question=question
    )

    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content, documents
