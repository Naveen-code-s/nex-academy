from core.llm import get_llm


def summarize_documents(documents):

    if not documents:

        return "No document content available."

    content = "\n\n".join(
        document.page_content
        for document in documents
    )

    # Avoid sending an extremely large paper
    content = content[:30000]

    prompt = f"""
You are NEXUS AI, an academic research assistant.

Summarize the following research paper content.

Provide:

1. Research Objective
2. Problem Addressed
3. Methodology
4. Dataset / Experimental Setup
5. Main Results
6. Key Findings
7. Conclusion
8. Limitations if available

Rules:

- Use only the provided content.
- Do not invent information.
- If something is unavailable, say "Not specified".
- Keep the summary clear and useful for a researcher.

Paper Content:

{content}
"""

    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    return response.content