from langchain_groq import ChatGroq

from config import GROQ_API_KEY, LLM_MODEL


def get_llm():
    """
    Create and return the Groq LLM.
    """

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Please add it to your .env file."
        )

    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=LLM_MODEL,
        temperature=0
    )