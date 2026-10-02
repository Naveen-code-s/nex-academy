from core.llm import get_llm


def extract_key_information(documents):

    if not documents:

        return "No document content available."

    content = "\n\n".join(
        document.page_content
        for document in documents
    )

    content = content[:30000]

    prompt = f"""
You are NEXUS AI, an academic research information extraction assistant.

Extract structured information from the research paper below.

Return exactly these sections:

## Title
## Authors
## Publication Year
## Research Problem
## Objective
## Methodology
## Dataset
## Models / Algorithms
## Evaluation Metrics
## Main Results
## Key Findings
## Conclusion
## Limitations

Rules:

- Use ONLY the provided paper content.
- Never invent missing information.
- Write "Not specified" when information is unavailable.
- Keep each section concise.

Paper:

{content}
"""

    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    return response.content