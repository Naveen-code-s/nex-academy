from dataclasses import dataclass
from datetime import datetime


@dataclass
class DocumentRecord:

    filename: str

    file_type: str

    uploaded_at: str

    pages: int = 0

    chunks: int = 0


def create_document_record(
    filename,
    file_type,
    pages=0,
    chunks=0,
):

    return DocumentRecord(
        filename=filename,
        file_type=file_type,
        uploaded_at=datetime.now().isoformat(),
        pages=pages,
        chunks=chunks,
    )