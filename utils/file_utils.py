from pathlib import Path


SUPPORTED_DOCUMENTS = {
    ".pdf",
    ".docx",
    ".txt"
}

SUPPORTED_DATA = {
    ".csv",
    ".xlsx"
}


def get_file_extension(
    file_name
):

    return Path(
        file_name
    ).suffix.lower()


def is_document(
    file_name
):

    return get_file_extension(
        file_name
    ) in SUPPORTED_DOCUMENTS


def is_data_file(
    file_name
):

    return get_file_extension(
        file_name
    ) in SUPPORTED_DATA