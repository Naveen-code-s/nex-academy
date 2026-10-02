from agents.research_agent import research_agent
from agents.search_agent import search_agent
from agents.data_agent import data_agent


def route_query(
    vector_store,
    query,
    mode="research",
    file_path=None,
):

    if mode == "search":

        return search_agent(
            vector_store,
            query,
        )

    if mode == "data":

        if not file_path:

            raise ValueError(
                "file_path is required for data mode."
            )

        return data_agent(
            file_path
        )

    return research_agent(
        vector_store,
        query,
    )