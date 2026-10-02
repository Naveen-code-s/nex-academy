import json
from pathlib import Path


DATABASE_FILE = Path(
    "data/processed/documents.json"
)


def save_documents(records):

    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = []

    for record in records:

        if hasattr(
            record,
            "__dict__",
        ):

            data.append(
                record.__dict__
            )

        else:

            data.append(record)

    DATABASE_FILE.write_text(
        json.dumps(
            data,
            indent=2,
        ),
        encoding="utf-8",
    )


def load_documents():

    if not DATABASE_FILE.exists():

        return []

    try:

        return json.loads(
            DATABASE_FILE.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError:

        return []