from analytics.data_analyzer import (
    load_data,
    get_data_summary,
)


def data_agent(file_path):

    dataframe = load_data(
        file_path
    )

    summary = get_data_summary(
        dataframe
    )

    return {
        "type": "data",
        "dataframe": dataframe,
        "summary": summary,
    }